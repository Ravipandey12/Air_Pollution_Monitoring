import users  
import pollution as poll  

def main():
    print("Air Quality Monitoring System!")
    api_key = "ab60a18f0ebf05c6dcd549d921efd4be"  # API key 

    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")

        choice = input("Please select an option: ")

        if choice == "1":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            nickname = input("What is your nickname? ")
            result = users.register_user(email, password, nickname)
            print(result)

        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            login_result = users.verify_login(email, password)
            print(login_result)

            if login_result == "Login successful":
                city = input("Enter your city name: ")
                pollution_data = poll.getPollutionData(city, api_key)

                if pollution_data is not None:
                    aqi = pollution_data["aqi"]
                    print(f"AQI of {city}: {aqi}")
                    
                    # Display pollutants information:
                    print("Pollutants Information:")
                    print(f"PM2.5: {pollution_data['pm2_5']}")
                    print(f"PM10: {pollution_data['pm10']}")
                    print(f"Ozone (O3): {pollution_data['o3']}")
                    print(f"NO2: {pollution_data['no2']}")
                    print(f"SO2: {pollution_data['so2']}")
                    print(f"CO: {pollution_data['co']}")

                    suggestion = poll.getSuggestion(aqi)
                    print(suggestion)
                else:
                    print("Error fetching AQI data. Please try again.")

        elif choice == "3":
            email = input("Enter your registered email: ")
            nickname = input("What is your nickname? ")
            new_password = input("Enter your new password: ")
            reset_result = users.forgot_password(email, nickname, new_password)
            print(reset_result)

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
