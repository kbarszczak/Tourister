![231571103-edd5bac9-deb4-48bb-ac9c-15984fe51c7e](https://user-images.githubusercontent.com/72699445/231577842-766443d0-64c4-4ab2-9e72-df3c69938031.png)

The application helps tourists visit interesting places. The main idea is to use the input text from the user to create the interests vector and therefore recommend the best-fitting places in the visited city. The application not only finds the best-fitting places but also creates a comprehensive visiting plan according to user requirements.

## Build status

Currently, we are building the proof of concept. However, there is going to be deployed a web application once we prove that the system works well.

## Screenshots

The following image shows the places in Krakow sorted by the best-matching ones.

![download (1)](https://user-images.githubusercontent.com/72699445/232027952-b2d0f782-af19-4091-8cc4-89b5a43cbd5f.png)

and another example

![download1](https://user-images.githubusercontent.com/72699445/232027894-c0a61353-87ab-4707-a5c4-72c102d22904.png)

The application layout
**todo: paste the app layout image**

## Usage

First of all clone the repository
```
mkdir Tourister
cd Tourister
git clone https://github.com/kbarszczak/Tourister .
```

The next step is to install the requirements
```
pip install -r requirements.txt
```

Now the application is ready for lunch. Just run the main.py
```
python app/main.py
```

## Possible improvements

There are some things that may be improved. Those are some of them:
- find a better places description to create an interest vector more precisely related to the place
- modify the training dataset and create it by taking more reliable data
