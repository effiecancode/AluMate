from rest_framework import serializers


class CommaSeparatedWordsField(serializers.ListField):
    def to_representation(self, value):
        return [word.strip() for word in value.split(",")]

    def to_internal_value(self, data):
        return data


# /home/john/Downloads/elp_test_data.xlsx-Sheet1.csv
