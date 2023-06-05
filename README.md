# Auctions

This Django-based web application enables users to create, bid on, and manage auctions for various items. The goal is to replicate the functionality of popular auction websites while providing users with an intuitive and interactive auction experience.

## Features

- User Registration: Users can create an account to participate in auctions.
- Auction Creation: Registered users can create new auction listings by specifying item details, including a starting bid and auction duration.
- Bidding: Users can place bids on active auctions, and the highest bid at the end of the auction wins.
- Listing Management: Users have the ability to edit or close their own auction listings.
- Watchlist: Users can add auctions to their watchlist to keep track of items they are interested in.
- Categories: Auction listings can be categorized to help users easily find items of their interest.
- User Authentication: Secure user authentication system to ensure only authorized users can access certain features.

## How to Run the Application

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd auctions`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Apply database migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`
6. Access the application in your web browser at: `http://localhost:8000`

## Future Work

In the future, I plan to enhance the frontend of the application to improve its overall design and user experience. Additionally, I aim to make the application fully responsive, ensuring it works seamlessly across different devices and screen sizes.

## Credits

This project is part of the CS50W (Web Programming with Python and JavaScript) course. For more detailed information and resources, please visit the [CS50W website](https://cs50.harvard.edu/web/).
