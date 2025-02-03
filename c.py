 def delete(self, request, *args, **kwargs):
       
        user = request.user

        try:
            # Check if the logged-in user is a doctor
            if user.role != "Doctor":
                return Response(
                    {"message": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Delete related data if the user is a doctor
            if hasattr(user, 'doctor'):
                doctor = user.doctor

                # 1. Delete appointments and related data
                if hasattr(doctor, 'appointments'):
                    appointments = doctor.appointments.all()
                    for appointment in appointments:
                        # Delete consultation summaries, prescriptions, and doctor's notes related to the appointment
                        if hasattr(appointment, 'consultation_summary'):
                            appointment.consultation_summary.delete()
                        if hasattr(appointment, 'prescriptions'):
                            appointment.prescriptions.all().delete()
                        if hasattr(appointment, 'doctors_notes'):
                            appointment.doctors_notes.all().delete()

                        # Finally, delete the appointment
                        appointment.delete()

                # 2. Delete doctor's account details
                if hasattr(doctor, 'account_details'):
                    doctor.account_details.all().delete()

                # 3. Delete transactions related to the doctor
                if hasattr(doctor, 'transactions'):
                    doctor.transactions.all().delete()

                # 4. Delete reviews written for the doctor
                if hasattr(doctor, 'reviews'):
                    doctor.reviews.all().delete()

                # 5. Delete education, media, and skills
                if hasattr(doctor, 'education'):
                    doctor.education.all().delete()
                if hasattr(doctor, 'media'):
                    doctor.media.all().delete()
                if hasattr(doctor, 'skills'):
                    doctor.skills.clear()  # ManyToMany field, clear it

                # 6. Finally, delete the Doctor object
                doctor.delete()

            # Delete the user
            user.delete()

            return Response(
                {"message": "Doctor account and all related data deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"message": f"Error deleting account: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
                