# PeaceGuardianBot
Domestic violence towards women.
Link to the video: https://youtube.com/shorts/S92HRDI_kq0?feature=share

Domestic violence is a widespread issue that affects numerous individuals worldwide, 
crossing geographical, cultural, and socioeconomic boundaries. Addressing this problem 
systematically is crucial due to its prevalence. While there is available data on domestic violence, 
the challenge lies in synthesizing and understanding the patterns, contributing factors, and 
variations across different regions. This complexity requires a comprehensive approach to 
analyze and derive meaningful insights from the dataset.  
Our project aims to utilize a dataset encompassing incidents of domestic violence 
worldwide to contribute to a deeper understanding of this critical issue. Through the use of 
advanced data analysis, machine learning techniques, and visualization tools, we aim to extract 
valuable insights that can inform policymakers, researchers, and organizations working towards 
mitigating the impact of domestic violence. 

Violence against women has a global impact, affecting women of all ages, classes, races, 
and ethnicities. Recent estimates indicate that 30 percent of women aged 15 or older worldwide 
have experienced physical and/or sexual intimate partner violence during their lifetime. This type 
of violence is the leading cause of homicide death in women globally and has significant health 
consequences. The economic and social costs associated with violence against women are 
substantial, and global evidence demonstrates that it consistently hinders development efforts at 
various levels, leading to the depreciation of physical, human, and social capital. Our goal in 
working on this project is to contribute to the improvement of the situation of domestic violence 
around the world.

Information about the data.
The dataset encompasses information spanning from 2000 to 2024, covering a variety of forms of violence and associated measures to combat them. Utilizing this dataset, we have created a sophisticated model capable of predicting the accuracy and efficacy of different measures and forms of violence based on the country in question.

Description of the ML/DL models we used with some theory.
In our model, we utilized several libraries and packages, including 'pandas' for data manipulation and analysis, 'Scikit-learn (sklearn)' for machine learning tasks such as preprocessing and model evaluation. Scikit-learn is a widely used open-source machine learning library written in Python that offers an array of methods for classification, regression, covariance matrix estimation, dimensionality reduction, data pre-processing, and benchmark problem generation. Additionally, we used 'joblib' for saving and loading trained models, 'telegram' for building a Telegram bot, 'matplotlib' for data visualization, and 'os' for operating system-related tasks.

Our model aims to determine the most common form of violence per country by grouping the data by country and finding the mode of 'Form of Violence' for each country. To accomplish this, we utilized the train_test_split method from scikit-learn, which provides efficient tools for data analysis and modeling, to split the dataset conveniently into training and test sets.

We trained a RandomForestClassifier model with 100 estimators on the training data. This choice was made due to the classifier's capability of handling multiple classes directly.

In conclusion, our project represents a holistic and data-driven approach to addressing domestic violence. By continually refining our methodologies and leveraging emerging technologies, we hope to make meaningful contributions to the ongoing efforts aimed at preventing and mitigating the impacts of domestic violence worldwide.
