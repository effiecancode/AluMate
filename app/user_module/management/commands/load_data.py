import os

import pandas as pd
from django.core.management.base import BaseCommand

from app.user_module.models import UserData


class Command(BaseCommand):
    help = "Import data from an Excel file into the ImportedUserData model"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="The path to the Excel file"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        try:
            df = pd.read_excel(file_path)
            records = df.to_dict("records")

            for record in records:
                PF = record.get("PF")
                if pd.isna(PF):  # Check for NaN using pandas isna() function
                    PF = None

                scholar_code = record.get("scholar_code")
                if pd.isna(
                    scholar_code
                ):  # Check for NaN using pandas isna() function
                    scholar_code = None

                imported_user_data = UserData.objects.create(  # noqa [F841]
                    # username=record["username"],
                    # first_name=record["first_name"],
                    # last_name=record["last_name"],
                    # email=record["email"],
                    scholar_type=record["scholar_type"],
                    PF=PF,
                    scholar_code=scholar_code,
                )
                # You can perform additional comparison or analysis here based on the imported data.
                # For example, compare the data with existing records in the User model.

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported data to ImportedUserData from {file_path}"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
