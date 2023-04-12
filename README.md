![banner](https://user-images.githubusercontent.com/72699445/231571103-edd5bac9-deb4-48bb-ac9c-15984fe51c7e.png)

The application helps tourists visit interesting places. The main idea is to use the input text from the user to create the interests vector and therefore recommend the best-fitting places in the visited city. The application not only finds the best-fitting places but also creates a comprehensive visiting plan according to user requirements.

## The results

The following image shows the places in Krakow sorted by the best-matching ones.

![download](https://user-images.githubusercontent.com/72699445/231575278-af3412b4-4c60-41f1-9868-8d0b179027fa.png)

and another example

![download (1)](https://user-images.githubusercontent.com/72699445/231575879-950f39d2-0a86-4c6f-a9aa-19265af6a917.png)

The application layout
**todo: paste the app layout image**

## Usage

First of all clone the repository
```
mkdir Tourister
cd Tourister
git clone https://github.com/kbarszczak/Tourister .
```

Next step is to install the requirements
```
pip install -r requirements.txt
```

Now the application is ready to lunch. Just run the main.py
```
python app/main.py
```

## Possible improvements

There are some things that may be improved. Those are some of them:
- find a better places description to create an interest vector more precisely related with the place
- modify the training dataset and create it by taking more reliable data
