# first start the SQL server by running 'net start MySQL80' with admin
# then open MySQL and make sure the server is running
# then run this script

import mysql.connector
from faker import Faker
from datetime import datetime
import random
from shapely import wkt

# main
def main():
    
    # fake = Faker()

    try:
        # connection = create_connection()
        connection = create_connection_AWS()
        cursor = connection.cursor()

        # create_database_query = "CREATE DATABASE IF NOT EXISTS cadmus_db"
        # cursor.execute(create_database_query)

        # Generate n agencies with m medics with o reports each
        for _ in range(3):
            generateAgency(cursor)
            agency_uid = cursor.lastrowid
            for _ in range(5):
                generateMedic(cursor, agency_uid)
                medic_uid = cursor.lastrowid
                for _ in range(10):
                    generateReport(cursor,medic_uid)

        # Commit the changes
        connection.commit()

        print("Fake data inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")


# ----------------------------------- helper functions -------------------------------------


# Function to create a connection to local MySQL database
def create_connection():
    return mysql.connector.connect(
        user="root",
        password="Zj5$q26]}~R6",
        database="cadmus_db"
    )


# Function to create a connection to AWS MySQL database
def create_connection_AWS():
    return mysql.connector.connect(
        host="cadmusdbtest.csaevtj8flgb.us-east-1.rds.amazonaws.com",
        user="root",
        password="Zj5$q26]}~R6",
        database="CADMUS_db",
        port=3306
    )


# Generate a fake EMS agency
def generateAgency(cursor):
    fake = Faker()
    agency_data = (
        fake.email(),               # email
        (fake.company() + ' EMS'),  # agency_name
        'pass',                     # password
        generate_timestamp(),       # registered_timestamp
        generate_timestamp(),       # last_login_timestamp
        fake.uuid4(),               # access_token
        random.randint(1, 100),     # reports_processed
        fake.word(),                # ePCR_provider
        fake.word(),                # nemsis_agency_name
        random.randint(1000, 9999)  # nemsis_agency_number
    )

    cursor.execute("""
        INSERT INTO agencies (
            email,
            agency_name,
            password,
            registered_timestamp,
            last_login_timestamp,
            access_token,
            reports_processed,
            ePCR_provider,
            nemsis_agency_name,
            nemsis_agency_number
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, agency_data)

    return agency_data


# Generate a fake medic
def generateMedic(cursor,agency_uid):
    fake = Faker()
    medic_data = (
        fake.name(),                # medic_name
        fake.email(),               # medic_email
        agency_uid                  # agencies_uid
    )

    cursor.execute("""
        INSERT INTO medics (
            medic_name,
            medic_email,
            agencies_uid
        ) VALUES (%s, %s, %s)
    """, medic_data)

    return medic_data


# Generate a fake report
def generateReport(cursor,medic_uid):
    fake = Faker()
    report_data = (
        # f"POINT({fake.longitude()} {fake.latitude()})",  # vehicle_dispatch_gps_location
        fake.numerify('######-#######'),    # vehicle_dispatch_national_grid_location
        fake.pyfloat(),                     # beginning_odom_readings
        fake.pyfloat(),                     # on_scene_odom_readings
        fake.pyfloat(),                     # patient_destination_odom_readings
        fake.pyfloat(),                     # ending_odom_readings
        fake.random_int(),                  # response_mode_to_scene
        fake.random_int(),                  # dispatch_priority
        fake.date_time(),                   # call_time
        fake.date_time(),                   # unit_notified
        fake.date_time(),                   # dispatch_time
        fake.date_time(),                   # dispatch_ack
        fake.date_time(),                   # unit_on_route
        fake.date_time(),                   # unit_arrived_on_scene
        fake.date_time(),                   # unit_arrived_at_patient
        fake.date_time(),                   # transfer_of_ems_care
        fake.date_time(),                   # unit_left_scene
        fake.date_time(),                   # arrival_at_dest_landing_area
        fake.date_time(),                   # patient_at_destination
        fake.date_time(),                   # destination_transfer_of_care
        fake.date_time(),                   # unit_back_in_service
        fake.date_time(),                   # unit_cancelled
        fake.date_time(),                   # unit_home
        fake.date_time(),                   # ems_call_completed
        fake.date_time(),                   # arrival_at_staging
        fake.random_int() % 2,              # pcs
        fake.random_int() % 2,              # pcs_signed
        fake.pyfloat(),                     # milage_to_closest_hospital
        fake.random_int(),                  # num_patients_at_scene
        # f"POINT({fake.longitude()} {fake.latitude()})",  # scene_gps_location
        fake.numerify('######-#######'),    # scene_national_grid_coordinates
        fake.word(),                        # primary_symptom
        fake.word(),                        # primary_impression
        fake.random_int(),                  # cardiac_arrest
        fake.random_int(),                  # resuscitation_attempted
        fake.random_int(),                  # return_of_circulation
        fake.date_time(),                   # time_of_resuscitation
        fake.date_time(),                   # resuscitation_discontinued
        fake.date_time(),                   # initial_time_of_cpr
        fake.word(),                        # medical_history
        # f"POINT({fake.longitude()} {fake.latitude()})",  # destination_gps_location
        fake.numerify('######-#######'),    # destination_national_grid_location
        fake.random_int(),                  # num_patients_transported
        fake.random_int(),                  # level_of_care_provided
        fake.word(),                        # reportscol
        fake.text(),                        # narrative
        fake.pyfloat(),                     # dispatch_to_scene_odom
        fake.pyfloat(),                     # dispatch_to_patient_dest_odom
        fake.pyfloat(),                     # dispatch_to_end_odom
        fake.pyfloat(),                     # on_scene_to_end_odom
        fake.random_int(),                  # call_notified_time
        fake.random_int(),                  # notified_to_en_route_time
        fake.random_int(),                  # driving_time
        fake.random_int(),                  # notified_to_complete_time
        fake.random_int(),                  # scene_to_patient_time
        fake.random_int(),                  # total_on_scene_time
        fake.random_int(),                  # patient_to_destination_time
        fake.random_int(),                  # care_by_crew_time
        fake.random_int(),                  # recovery_time
        fake.random_int() % 2,              # response_mode_matches_level_of_care_test
        fake.random_int() % 2,              # pcs_obtained_for_bls
        fake.random_int() % 2,              # pcs_has_signature_test
        fake.random_int() % 2,              # dispatch_priority_matches_dispatch_test
        fake.random_int() % 2,              # pcs_date_test
        fake.random_int() % 2,              # time_test
        fake.random_int() % 2,              # arrest_test
        fake.random_int() % 2,              # vitals_test
        fake.random_int() % 2,              # procedures_valid_test
        fake.random_int() % 2,              # closest_hospital_chosen_test
        fake.random_int() % 2,              # odom_to_dest_test
        fake.random_int() % 2,              # odom_to_scene_test
        fake.random_int() % 2,              # pcs_symptom_test
        fake.random_int() % 2,              # pcs_impression_test
        fake.random_int() % 2,              # failed_to_resuscitate_test
        fake.random_int() % 2,              # medical_history_test
        fake.random_int() % 2,              # medication_history_test
        fake.random_int() % 2,              # two_sets_vitals_test
        fake.random_int() % 2,              # pain_scale_test
        fake.random_int() % 2,              # ecg_recorded_output_test
        fake.random_int() % 2,              # narrative_exists
        medic_uid                           # medics_medic_uid
    )

    cursor.execute("""
        INSERT INTO reports (
            -- vehicle_dispatch_gps_location,
            vehicle_dispatch_national_grid_location,
            beginning_odom_readings,
            on_scene_odom_readings,
            patient_destination_odom_readings,
            ending_odom_readings,
            response_mode_to_scene,
            dispatch_priority,
            call_time,
            unit_notified,
            dispatch_time,
            dispatch_ack,
            unit_on_route,
            unit_arrived_on_scene,
            unit_arrived_at_patient,
            transfer_of_ems_care,
            unit_left_scene,
            arrival_at_dest_landing_area,
            patient_at_destination,
            destination_transfer_of_care,
            unit_back_in_service,
            unit_cancelled,
            unit_home,
            ems_call_completed,
            arrival_at_staging,
            pcs,
            pcs_signed,
            milage_to_closest_hospital,
            num_patients_at_scene,
            -- scene_gps_location,
            scene_national_grid_coordinates,
            primary_symptom,
            primary_impression,
            cardiac_arrest,
            resuscitation_attempted,
            return_of_circulation,
            time_of_resuscitation,
            resuscitation_discontinued,
            initial_time_of_cpr,
            medical_history,
            -- destination_gps_location,
            destination_national_grid_location,
            num_patients_transported,
            level_of_care_provided,
            reportscol,
            narrative,
            dispatch_to_scene_odom,
            dispatch_to_patient_dest_odom,
            dispatch_to_end_odom,
            on_scene_to_end_odom,
            call_notified_time,
            scene_to_patient_time,
            total_on_scene_time,
            notified_to_en_route_time,
            driving_time,
            notified_to_complete_time,
            patient_to_destination_time,
            care_by_crew_time,
            recovery_time,
            response_mode_matches_level_of_care_test,
            pcs_obtained_for_bls,
            pcs_has_signature_test,
            dispatch_priority_matches_dispatch_test,
            pcs_date_test,
            time_test,
            arrest_test,
            vitals_test,
            procedures_valid_test,
            closest_hospital_chosen_test,
            odom_to_dest_test,
            odom_to_scene_test,
            pcs_symptom_test,
            pcs_impression_test,
            failed_to_resuscitate_test,
            medical_history_test,
            medication_history_test,
            two_sets_vitals_test,
            pain_scale_test,
            ecg_recorded_output_test,
            narrative_exists,
            medics_medic_uid
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, report_data)

    return report_data


# Generate a random timestamp - change to progressive timestamps eventually
def generate_timestamp():
    return int(datetime.timestamp(datetime.now()))


# --------------------------------- end helper functions -----------------------------------

if __name__ == "__main__":
    main()
