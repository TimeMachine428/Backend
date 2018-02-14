from .job import Job
import importlib.util
import os


class TestCaseJob(Job):

    # Define this class as a proxy class, since we don't want multi-table inheritance in this case
    class Meta:
        proxy = True

    def execute(self):
        module_path = self.save_code()

        try:
            spec = importlib.util.spec_from_file_location("module", os.path.join(module_path, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except SyntaxError as err:
            return err

        method = getattr(module, self.method, None)

        if method is None:
            return ValueError("Required method %s is unavailable" % self.method)

        if not callable(method):
            return ValueError("Required method %s is not callable" % self.method)

        meta = self.decode_meta()
        args = meta.get('args', [])
        kwargs = meta.get('kwargs', {})

        try:
            result = method(*args, **kwargs)
        except Exception as e:
            return e

        if result == meta['result']:
            return True
