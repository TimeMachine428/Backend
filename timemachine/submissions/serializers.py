from rest_framework import serializers
from submissions.models import Job
from restapi.models import TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    problem = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TestCase
        fields = ('id', 'method', 'inputs', 'outputs', 'problem')


class JobSerializer(serializers.ModelSerializer):
    testcase = TestCaseSerializer()

    class Meta:
        model = Job
        fields = ('id', 'testcase', 'name', 'completed', 'success', 'error', 'execution_time_millis')
