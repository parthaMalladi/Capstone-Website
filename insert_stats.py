from schemas import DiabetesStats, StrokeStats, HeartDiseaseStats
from db import db_session

'''
# insert averages for diabetes
diabetes_stats = DiabetesStats(
    average_pregnancies='3',
    average_glucose='110',
    average_blood_pressure='68',
    average_skin_thickness='20',
    average_insulin='69',
    average_bmi='30',
    average_diabetes_pedigree_function='0.43',
    average_age='31'
)
db_session.add(diabetes_stats)

# insert averages for stroke
stroke_stats = StrokeStats(
    average_gender = 'Male',
    average_age='42',
    average_hypertension='0',
    average_heart_disease='0',
    average_ever_married='Yes',
    average_work_type='Private',
    average_residence_type='Urban',
    average_avg_glucose_level='105',
    average_bmi='28.8',
    average_smoking_status='never smoked'
)
db_session.add(stroke_stats)

# insert averages for heart disease
heart_stats = HeartDiseaseStats(
    average_age='50',
    average_sex='F',
    average_resting_bp='130',   
    average_cholesterol='227',
    average_fasting_bs='0',
    average_ecg='Normal',
    average_max_hr='148',
    average_exercise_angina='N',
    average_oldpeak='0.41',
    average_st_slope='Up'
)
db_session.add(heart_stats)
'''

'''
# insert averages for diabetes
diabetes_stats = DiabetesStats(
    average_pregnancies='https://www.niddk.nih.gov/health-information/diabetes/diabetes-pregnancy',
    average_glucose='https://www.northeastmedicalgroup.org/articles/what-is-healthy-blood-sugar',
    average_blood_pressure='https://www.hopkinsmedicine.org/health/conditions-and-diseases/diabetes/diabetes-and-high-blood-pressure',
    average_skin_thickness='https://www.ncbi.nlm.nih.gov/books/NBK481900/',
    average_insulin='https://www.veri.co/learn/optimal-fasting-insulin-level?srsltid=AfmBOoo_40qWIVtWcVOTucNXnz3hbKN3vDplcTL060pGT4Mv-XuwAv2k',
    average_bmi='https://www.heart.org/en/healthy-living/healthy-eating/losing-weight/bmi-in-adults#:~:text=A%20BMI%20between%2018.5%20and,or%20higher%20is%20considered%20obese.',
    average_diabetes_pedigree_function='',
    average_age='https://www.medicalnewstoday.com/articles/317375#:~:text=The%20average%20age%20of%20onset%20for%20type%202%20diabetes&text=The%20onset%20of%20diabetes%20is,can%20occur%20at%20any%20age.'
)
db_session.add(diabetes_stats)

# insert averages for stroke
stroke_stats = StrokeStats(
    average_gender = 'https://www.ahajournals.org/doi/10.1161/CIRCRESAHA.121.319915',
    average_age='https://pmc.ncbi.nlm.nih.gov/articles/PMC6535078/#:~:text=Aging%20is%20the%20most%20robust,persons%20aged%20%E2%89%A565%20years.',
    average_hypertension='https://www.heart.org/en/health-topics/high-blood-pressure/health-threats-from-high-blood-pressure/how-high-blood-pressure-can-lead-to-stroke',
    average_heart_disease='https://pmc.ncbi.nlm.nih.gov/articles/PMC9945299/',
    average_ever_married='https://www.mountsinai.org/files/MSHealth/Assets/HS/Locations/Precision-Recovery/BLOG%2011.pdf#:~:text=A%20recent%20study%20showed%20that%20the%20risk,stroke%20more%20than%20simply%20being%20married%20(2).',
    average_work_type='https://pmc.ncbi.nlm.nih.gov/articles/PMC10574301/',
    average_residence_type='https://pubmed.ncbi.nlm.nih.gov/34087323/',
    average_avg_glucose_level='https://www.ahajournals.org/doi/10.1161/01.str.0000115297.92132.84',
    average_bmi='https://www.heart.org/en/healthy-living/healthy-eating/losing-weight/bmi-in-adults#:~:text=A%20BMI%20between%2018.5%20and,or%20higher%20is%20considered%20obese.',
    average_smoking_status='https://www.world-stroke.org/assets/downloads/STROKE_RISK_AND_PREVENTION_LEAFLET_SMOKING-EN.pdf'
)
db_session.add(stroke_stats)

# insert averages for heart disease
heart_stats = HeartDiseaseStats(
    average_age='https://pmc.ncbi.nlm.nih.gov/articles/PMC6616540/',
    average_sex='https://pmc.ncbi.nlm.nih.gov/articles/PMC6616540/',
    average_resting_bp='https://utswmed.org/medblog/high-blood-pressure-heart-disease/#:~:text=For%20the%20average%20person%20who,at%20risk%20for%20heart%20disease.',   
    average_cholesterol='https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/symptoms-causes/syc-20350800#:~:text=Prevention,drinks%20a%20day%20for%20men.',
    average_fasting_bs='https://www.cdc.gov/diabetes/diabetes-complications/diabetes-and-your-heart.html',
    average_ecg='https://www.mayoclinic.org/tests-procedures/ekg/about/pac-20384983',
    average_max_hr='https://www.health.harvard.edu/heart-health/what-your-heart-rate-is-telling-you',
    average_exercise_angina='https://www.health.harvard.edu/heart-health/angina-symptoms-diagnosis-and-treatments#:~:text=Angina%20(pronounced%20ANN%2Djuh%2Dnuh%20or%20ann%2DJIE%2Dnuh)%20is%20pain,which%20is%20caused%20by%20cholesterol%2Dclogged%20coronary%20arteries.',
    average_oldpeak='',
    average_st_slope='https://www.sciencedirect.com/science/article/abs/pii/0002870386902656#:~:text=Abstract,compared%20favorably%20with%20TI%20imaging.'
)
db_session.add(heart_stats)
'''

# commit all and close session
db_session.commit()
db_session.close()
