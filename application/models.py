from hashlib import new
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.forms.models import ModelFormOptions, model_to_dict
import random
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class topic(models.Model):
    topic_name = models.CharField(max_length=255)


class exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/exercise_icon', null=True)
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, null=True)
    created_date = models.DateField(auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class condition(models.Model):
    key = models.CharField(max_length=15, null=True)
    limit = models.IntegerField(null=True)
    query = models.CharField(max_length=255)


class question_element(models.Model):
    label = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    is_random = models.BooleanField(default=False)
    conditions = models.ManyToManyField(condition, null=True)
    example_value = models.CharField(max_length=255)

    def get_joined_condition_list(self):
        condition_list = self.conditions.all()
        new_list = []
        for i in condition_list:
            single_string = f'NUMBER {i.key} {i.limit}'
            new_list.append(single_string)

        condition_string = " and ".join(new_list)
        return condition_string


class question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(exercise, on_delete=models.CASCADE, null=True)
    question_elements = models.ManyToManyField(question_element)
    criteria = models.CharField(max_length=255, null=True)
    loop = models.IntegerField(null=True)
    success_message = models.TextField(null=True)
    failure_message = models.TextField(null=True)
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_correct_random_value(self, condition):
        temp_con = ""

        while True:
            random_value = random.randint(0, 500)
            temp_con = condition.replace("NUMBER", str(random_value))
            if eval(temp_con):
                return random_value

    def get_question_versions(self):

        container = []

        for i in range(self.loop):
            data = {'s_no': i+1}
            temp_expression = self.criteria

            for single_question_element in self.question_elements.all():
                if single_question_element.is_random:
                    my_all_conditions = single_question_element.get_joined_condition_list()
                    value = self.get_correct_random_value(my_all_conditions)
                    # print(value)
                    # for single_condition in single_question_element.conditions.all():
                    #     print(i + 1)
                    #     my_condition = model_to_dict(single_condition)

                    #     whole_query = f'{} {my_condition['key']} {my_condition['limit']}'
                    #     print(my_condition)

                else:
                    value = single_question_element.value if single_question_element.value else f'{single_question_element.symbol}?'

                temp_expression = temp_expression.replace(
                    single_question_element.symbol,
                    str(value)
                )

            data['expression'] = temp_expression
            container.append(data)

        return container
        # print(container)
