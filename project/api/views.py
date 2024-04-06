import os.path
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from django.conf import settings
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import shutil


@api_view(['POST'])
def backup_files(request):
    source_folder_path = os.path.join(settings.BASE_DIR,"static","export")
    destination_folder_path = os.path.join(settings.BASE_DIR,"static","backup")
    try:
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

        # Iterate over files in source folder and copy them to destination folder
        for filename in os.listdir(source_folder_path):
            source_file_path = os.path.join(source_folder_path, filename)
            destination_file_path = os.path.join(destination_folder_path, filename)
            shutil.copy(source_file_path, destination_file_path)

        return Response()
    except Exception as e:
        return Response(f"An error occurred: {e}")


@api_view(['GET'])
def file_list(request):
    directory = os.path.join(settings.BASE_DIR,"static","export")  # Path to your folder
    files = os.listdir(directory)
    return Response(files)
def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


import os
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt  # Only if you're allowing non-browser clients to access this endpoint
# def get_dynamic_file(request, filename):
#     # Logic to generate or fetch dynamically generated file content
#     file_path = os.path.join(settings.BASE_DIR,"static","export")
#
#     if os.path.exists(file_path):
#         # Return the file as a response
#         return FileResponse(open(file_path, 'rb'))
#     else:
#         return JsonResponse({'error': 'File not found'}, status=404)
#
def get_all_files(request):
    directory = os.path.join(settings.BASE_DIR,"static","export")
    # file_urls = [request.build_absolute_uri(os.path.join(directory, file_name)) for file_name in files]
    return JsonResponse({'path': directory})

# from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os
from reportlab.lib.pagesizes import A4


@api_view(['POST'])
def convert_pngs_to_pdf(request):
    # Create a PDF canvas
    png_folder = os.path.join(settings.BASE_DIR,"static","export")  # Path to the folder containing PNG files
    output_pdf_path =os.path.join(settings.BASE_DIR,"static","output.pdf")
    c = canvas.Canvas(output_pdf_path, pagesize=A4)

    # Get a list of all PNG files in the folder
    png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]

    # Sort the list of PNG files to ensure proper ordering
    png_files.sort()

    # Loop through each PNG file
    for png_file in png_files:
        # Open the PNG file
        img = Image.open(os.path.join(png_folder, png_file))

        width_ratio = A4[0] / img.width
        height_ratio = A4[1] / img.height
        scaling_factor = min(width_ratio, height_ratio)

        # Calculate the new dimensions of the image
        new_width = img.width * scaling_factor
        new_height = img.height * scaling_factor

        # Get the size of the PNG image
        # Draw the PNG image onto the PDF canvas
        c.drawImage(os.path.join(png_folder, png_file), 0, 0, new_width, new_height)

        # Add a new page for the next image
        c.showPage()

    # Save the PDF
    c.save()
    # Response = 0
    return Response({"path": os.path.join(settings.BASE_DIR, "static")})

# Example usage:
 # Path to save the output PDF file

@api_view(['GET'])
def main(request):
    df = pd.read_csv(os.path.join(settings.BASE_DIR, "static", 'marks1.csv'))
    data = [df.columns.tolist()] + df.values.tolist()

    # (x, y) coordinates of the text position
    font_path = "arial.ttf"  # Path to the font file
    font_size = 30
    text_color = (0, 0, 0)
    a = 0
    b = {}

    image_path = os.path.join(settings.BASE_DIR, "static", 'marksheet1.png')
    image = Image.open(image_path)

    export_data = [
    ]

    # Create PDF
    for i in data:

        if (a == 0):
            pass
        else:
            c = 0
            for j in i:
                b.append({f"{data[0][c]}": j})

                c += 1

            name_position = (908, 676)
            dob_bs_position = (537, 742)
            dob_ad_position = (1447, 742)
            reg_no_position = (609, 790)
            sym_no_position = (1474, 790)
            exam_date_bs_position = (1564, 849)
            exam_date_ad_position = (271, 909)
            date_of_issue_position = (563, 2730)
            gpa_position = (1738, 2220)

            name = b[0]['Name']
            dob_bs = b[1]['Date of Birth BS']
            dob_ad = b[2]['Date Of Birth AD']
            reg_no = b[3]['Registration No']
            sym_no = b[4]['Symbol No']
            exam_date_bs = b[5]['EXAM DATE (BS)']
            exam_date_ad = b[6]['EXAM DATE (AD)']
            date_of_issue = b[7]['DATE OF ISSUE']

            english_th = convert_to_int(b[8]['COM ENGLISH (TH)'])
            english_in =convert_to_int(b[9]['COM ENGLISH (IN)'])
            nepali_th =convert_to_int(b[10]['COM NEPALI (TH)'])
            nepali_in =convert_to_int( b[11]['COM NEPALI (IN)'])
            social_th =convert_to_int(b[12]['COM SOCIAL STUDIES (TH)'])
            social_in =convert_to_int(b[13]['COM SOCIAL STUDIES (IN)'])
            acc_th =convert_to_int(b[14]['PRINCIPLE OF ACCOUNTING (TH)'])
            acc_in =convert_to_int(b[15]['PRINCIPLE OF ACCOUNTING (IN)'])
            economics_th =convert_to_int(b[16]['ECONOMICS (TH)'])
            economics_in =convert_to_int( b[17]['ECONOMICS (IN)'])
            buss_th =convert_to_int(b[18]['BUSINESS STUDIES (TH)'])
            buss_in =convert_to_int(b[19]['BUSINESS STUDIES (IN)'])
            marks_75 =[english_th, nepali_th, social_th, acc_th, economics_th, buss_th]
            marks_25 = [english_in, nepali_in, social_in, acc_in, economics_in, buss_in]

            marks_75_grade = []
            marks_25_grade = []
            marks_75_GP = []
            marks_25_GP = []

            final_marks = [
                (english_th + english_in) if (type(english_th) != str and type(english_th) != str) else "NG",
                (nepali_th + nepali_in) if (type(nepali_th) != str and type(nepali_in) != str) else "NG",
                (social_th + social_in) if (type(social_th) != str and type(social_in) != str) else "NG",
                (acc_th + acc_in) if (type(acc_th) != str and type(acc_in) != str) else "NG",
                (economics_in + economics_th) if (type(economics_in) != str and type(economics_th) != str) else "NG",
                (buss_th + buss_in) if (type(buss_th) != str and type(buss_in) != str) else "NG"
            ]
            final_grade = []
            final_GP = []
            sum_GP = 0
            total_credit = 27

            for marks in marks_75:
                if (marks == "NG"):
                    marks_75_grade.append("NG")
                    marks_75_GP.append("NG")
                elif (marks == "ABS"):
                    marks_75_grade.append("ABS")
                    marks_75_GP.append("ABS")
                elif isinstance(marks, str):
                    marks_75_grade.append("NG")
                    marks_75_GP.append("NG")
                    # Handle the case where marks is a string other than "NG" or "ABS"
                    # You may want to add appropriate handling here based on your requirements
                    pass

                elif (marks >= 67.5):
                    marks_75_grade.append("A+")
                    marks_75_GP.append(4.0)
                elif (marks >= 60):
                    marks_75_grade.append("A")
                    marks_75_GP.append(3.6)

                elif (marks >= 52.5):
                    marks_75_grade.append("B+")
                    marks_75_GP.append(3.2)

                elif (marks >= 45):
                    marks_75_grade.append("B")
                    marks_75_GP.append(2.8)

                elif (marks >= 37.5):
                    marks_75_grade.append("C+")
                    marks_75_GP.append(2.4)

                elif (marks >= 30.5):
                    marks_75_grade.append("C")
                    marks_75_GP.append(2.0)

                elif (marks >= 26.25):
                    marks_75_grade.append("D")
                    marks_75_GP.append(1.6)
                else:
                    marks_75_grade.append("NG")
                    marks_75_GP.append("NG")

            for marks in marks_25:

                if isinstance(marks, str):
                    marks_25_grade.append("NG")
                    # marks_75_GP.append("NG")
                    # Handle the case where marks is a string other than "NG" or "ABS"
                    # You may want to add appropriate handling here based on your requirements
                    pass
                elif (marks >= 22.5):
                    marks_25_grade.append("A+")
                    marks_25_GP.append(4.0)

                elif (marks >= 20):
                    marks_25_grade.append("A")
                    marks_25_GP.append(3.6)

                elif (marks >= 17.5):
                    marks_25_grade.append("B+")
                    marks_25_GP.append(3.2)

                elif (marks >= 15):
                    marks_25_grade.append("B")
                    marks_25_GP.append(2.8)

                elif (marks >= 12.5):
                    marks_25_grade.append("C+")
                    marks_25_GP.append(2.4)

                elif (marks >= 10):
                    marks_25_grade.append("C")
                    marks_25_GP.append(2.0)

                elif (marks >= 7.5):
                    marks_25_grade.append("D")
                    marks_25_GP.append(1.6)
                else:
                    marks_25_grade.append("NG")
                    marks_25_GP.append("NG")


            for marks in final_marks:

                if isinstance(marks, str):
                    final_grade.append("NG")
                    final_GP.append("NG")
                    # Handle the case where marks is a string other than "NG" or "ABS"
                    # You may want to add appropriate handling here based on your requirements
                    pass

                elif (marks >= 90):
                    final_grade.append("A+")
                    final_GP.append(4.0)
                elif (marks >= 80):
                    final_grade.append("A")
                    final_GP.append(3.6)

                elif (marks >= 70):
                    final_grade.append("B+")
                    final_GP.append(3.2)

                elif (marks >= 60):
                    final_grade.append("B")
                    final_GP.append(2.8)

                elif (marks >= 50):
                    final_grade.append("C+")
                    final_GP.append(2.6)

                elif (marks >= 40):
                    final_grade.append("C")
                    final_GP.append(2.4)

                elif (marks >= 30):
                    final_grade.append("D")
                    final_GP.append(2.0)
                else:
                    final_grade.append("NG")
                    final_GP.append("NG")

            credithour = [
                [2.25, 3, 3.75, 3.75, 3.75, 3.75],
                [0.75, 1, 1.25, 1.25, 1.25, 1.25]
            ]

            # for d in range(len(final_grade)):
            #     sum_GP += final_GP[d]  * (credithour[0][d]+credithour[1][d])

            for d in range(len(marks_75_GP)):
                if isinstance(marks_75_GP[d], str):
                    sum_GP = "NG"
                    break
                elif (type(marks_75_GP[d]) == float):
                    sum_GP += marks_75_GP[d] * credithour[0][d]

            for d in range(len(marks_25_GP)):
                if (sum_GP == "NG"):
                    break
                elif isinstance(marks_25_GP[d], str):
                    sum_GP = "NG"
                    break
                elif (type(marks_25_GP[d]) == float):
                    sum_GP += marks_25_GP[d] * credithour[1][d]

            subjects = [
                ["COM ENGLISH (TH)", "COM NEPALI (TH)", "COM SOCIAL STUDIES (TH)", "PRINCIPLE OF ACCOUNTING (TH)",
                 "ECONOMICS (TH)", "BUSINESS STUDIES (TH)"],
                ["COM ENGLISH (IN)", "COM NEPALI (IN)", "COM SOCIAL STUDIES (IN)", "PRINCIPLE OF ACCOUNTING (IN)",
                 "ECONOMICS (IN)", "BUSINESS STUDIES (IN)"],
            ]

            final_GPA = (sum_GP) / 27 if (type(sum_GP) == float) else "NG"

            subject_code = [
                ["0031", "0011", "0051", "1031", "3031", "2151"],
                ["0032", "0012", "0052", "1032", "3032", "2152"],
            ]
            # Initialize drawing context
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            font_size = 40
            font_size1 = 32
            # Load font (if specified)
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
                font1 = ImageFont.truetype(font_path, font_size1)
            else:
                font = ImageFont.load_default()
                font1 = ImageFont.load_default()

            (subj_posx, subj_posy) = (213, 1276)

            export_json = {
                "name" : name,
                "GPA": final_GPA.__round__(2) if (type(final_GPA) == float) else final_GPA
            }
            export_data.append(export_json)
            posy = 0
            # print(marks_75)
            # print(marks_25)
            # print(final_marks)
            # print(final_grade)
            # Draw text on the image
            draw.text(name_position, name, fill=text_color, font=font)
            draw.text(dob_bs_position, dob_bs, fill=text_color, font=font)
            draw.text(dob_ad_position, dob_ad, fill=text_color, font=font)
            draw.text(reg_no_position, str(reg_no), fill=text_color, font=font)
            draw.text(sym_no_position, str(sym_no), fill=text_color, font=font)
            draw.text(exam_date_bs_position, exam_date_bs, fill=text_color, font=font)
            draw.text(exam_date_ad_position, exam_date_ad, fill=text_color, font=font)
            draw.text(date_of_issue_position, date_of_issue, fill=text_color, font=font)
            draw.text(gpa_position, str(final_GPA.__round__(2)) if type(final_GPA) == float else final_GPA,
                      fill=text_color, font=font)
            for l in range(6):
                draw.text((subj_posx, subj_posy), subject_code[0][l], fill=text_color, font=font1)
                draw.text((455, subj_posy), subjects[0][l], fill=text_color, font=font1)
                draw.text((1010, subj_posy), str(credithour[0][l]), fill=text_color, font=font1)
                draw.text((1240, subj_posy), str(marks_75_GP[l]), fill=text_color, font=font1)
                draw.text((1430, subj_posy), str(marks_75_grade[l]), fill=text_color, font=font1)
                posy = subj_posy + 20
                draw.text((1722, posy), str(final_grade[l]), fill=text_color, font=font1)

                subj_posy += 45
                draw.text((subj_posx, subj_posy), subject_code[1][l], fill=text_color, font=font1)
                draw.text((455, subj_posy), subjects[1][l], fill=text_color, font=font1)
                draw.text((1010, subj_posy), str(credithour[1][l]), fill=text_color, font=font1)
                draw.text((1240, subj_posy), str(marks_25_GP[l]), fill=text_color, font=font1)
                draw.text((1430, subj_posy), str(marks_25_grade[l]), fill=text_color, font=font1)

                subj_posy += 45

            export_path = os.path.join(settings.BASE_DIR, "static", "export", f'{b[0]['Name']}.png')
            image.save(export_path)

            # Show or save the image

        a += 1
        b = []

    return Response(export_data)
