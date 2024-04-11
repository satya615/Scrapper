from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"class": 'B_NuCI'})
        title_string = title.text.strip() if title else ""
    except Exception as e:
        print(f"Error extracting title: {e}")
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("div", attrs={'class': '_30jeq3 _16Jk6d'}).text.strip()
    except AttributeError:
        price = ""
    except Exception as e:
        print(f"Error extracting price: {e}")
        price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("div", attrs={'class': '_3LWZlK'}).text.strip()
    except AttributeError:
        rating = ""
    except Exception as e:
        print(f"Error extracting rating: {e}")
        rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'class': '_2_R_DZ'}).text.strip()
    except AttributeError:
        review_count = ""
    except Exception as e:
        print(f"Error extracting review count: {e}")
        review_count = ""
    return review_count

# Function to extract Availability Status
# def get_availability(soup):
#     try:
#         available = soup.find("div", attrs={'id': 'availability'}).text.strip()
#     except AttributeError:
#         available = "Not Available"
#     except Exception as e:
#         print(f"Error extracting availability: {e}")
#         available = ""
#     return available

if __name__ == '__main__':
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    URL = "https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    webpage = requests.get(URL, headers=HEADERS)
    

    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': '_1fQZEK'})
    links_list = []

    for link in links:
        href = link.get('href')
        if href.startswith("/"):
            links_list.append(href)
    print("https://www.flipkart.com"+links_list[0])
    d = {"title": [], "price": [], "rating": [], "reviews": []}
   
    for link in links_list:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
        
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        # availability = get_availability(new_soup)

    # amazon_df = pd.DataFrame.from_dict(d)
    # amazon_df['title'].replace('', np.nan, inplace=True)
    # amazon_df = amazon_df.dropna(subset=['title'])
    # amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(d)
