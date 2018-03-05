from .job import Job
import importlib.util
import collections
import os


class TestCaseJob(Job):

    # Define this class as a proxy class, since we don't want multi-table inheritance in this case
    class Meta:
        proxy = True

    def execute(self):
        # TODO: Implement custom errors for this module

        module_path = self.save_code()

        try:
            spec = importlib.util.spec_from_file_location("module", os.path.join(module_path, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except SyntaxError as err:
            return err

        method = getattr(module, self.testcase.method, None)

        if method is None:
            return ValueError("Required method %s is unavailable" % self.testcase.method)

        if not callable(method):
            return ValueError("Required method %s is not callable" % self.testcase.method)

        meta = self.decode_meta()
        args = meta.get('inputs', [])
        outputs = meta.get('outputs', [])

        try:
            result = method(*args)
        except Exception as e:
            return e

        if len(outputs) == 1 and outputs[0] == result:
            return True

        # Check the if result is a singleton, or tuple
        if isinstance(result, collections.Iterable) and len(result) == len(outputs):
            if all(r == o for r, o in zip(result, outputs)):
                return True
            else:
                return ValueError("Submission output doesn't match the expected result")
        else:
            return ValueError("Number of elements in the output doesn't match the number of expected elements")
