Language: English

# Sales and Purchases Manager and Organizer

## Presentation

Project to facilitate the management of a market or a company that handles little data that persists over time. The application allows you to manipulate, create and filter data, view a graph with the purchase expenses and download it, and export the data to csv or excel files.

## Functions

### Graph

An integrated arrow graph that shows expenses through sales. Integrated with an algorithm that allows it to be updated every time any of the data that has to do with money is changed. Its functions are graph and update_graph. You can download an image that contains the current graph of the application, the image will be located in the Downloads folder of your user.

### Logs

It has the logs function, so after running the app and moving a few things, you can review the logs.log file in the root of the project. The python loggin module and a custom function called logs are used

### Filter

A lot of data may be loaded and it may be a bit annoying to view it or search for a specific one, so above the project tree there is an input where by default you can search by product ID, if you need to search by name, date or cost you have an options menu to the right of the input to change the type of filtering. In order for these to work, the functions validate_is_numeric, validate_is_text, validate_input, filter_treeview and update_treeview were built.

### Exports

Below the product tree and next to the "sell" button, there are two buttons with different export options: Export to csv and export to excel. When you click on either of the two, the file will be downloaded to your user's Downloads folder. To provide this functionality, the pandas library was used within the export_to_excel and export_to_csv functions.

## Validations

The app comes with validations for certain actions:
When registering a product, the content of the fields is validated with regex to check if they are valid. You can see the patterns within the validate_name and validate_cost functions.
When filtering products, the menu and input will have validations to know exactly what type of filter you are setting, also validating if the value is numeric or text. You can see how it works within the validate_is_numeric, validate_is_text, validate_input and filter_treeview functions.

## Data management

To manipulate the data you want, you have different functions:

### Buy a product:

From here come the validations previously named, the purchase date is stored alone through the use of datetime and the ID is auto-incremental, so it is not necessary to specify it in the form. Within the app, you will only have to enter the "Name" of the product and the "Cost" of the same. The operation can be found in the create_element and buy functions.

### Selling a product:

You can sell a product by clicking on the one you want and pressing the "sell" button below the product tree. The idea is to save sales data as well as purchase data, but for the moment we are using a single table. The function delete_element works.

### Editing products:

Edit each product by double-clicking on it. Small fields will appear with information about the name and cost of the product. You can cancel the action or end it by clicking on any of the fields and pressing the "enter" key. Its functions are edit_element and save_edit.

## Getting started with the project

To run the application for the first time, you need to create your virtual environment, either with anaconda, virtualenvwrapper or the python virtual environments.

### virtualenvwrapper:

`mkvirtualenv my_env`

### Anaconda:

For Anaconda you can use Anaconda Navigator or the terminal if you have it in the environment variables, the second option would be:
`conda create --name my_env python=3.11.10`

#### to activate it:

`conda activate my_env`

### python virtual environments (venv):

`python -m venv my_env`

#### to activate it on Windows:

`my_env/Source/activate`

#### to activate it on Linux or Mac:

`source my_env/bin/activate`

### After having created and activated your environment, you must run the command `pip install -r requirements.txt` referencing the file that contains the project dependencies. After that you can run main.py and the app will work perfectly!

<hr>
Language: Spanish
<br>
<br>
<br>

# Gestor y organizador de Ventas y Compras de productos

## Presentación

Proyecto para facilitar la gestión de un mercado o una empresa que maneje pocos datos que persistan en el tiempo. La aplicación permite manipular, crear y filtrar datos, visualizar un grafico con los gastos de las compras y descargar el mismo, y exportar los datos a archivos csv o para excel.

# Funciones

### Grafico

Un grafico de flecha integrado que muestra los gastos a travéz de las ventas. Integrado con un algoritmo que permite que se actualize cada vez que se cambia alguno de los datos que tengan que ver con dinero. Sus funciones son graph y update_graph. Puede descargarse una imagen que contenga el grafico actual de la aplicación, la imagén estará hubicada en la carpeta Descargas de su usuario.

### Logs

Tiene la funcion de logs, así que despues de correr la app y mover un par de cosas, puede revisar el archivo logs.log en la raíz del proyecto. Se usa el modulo loggin de python y una función propia llamada logs

### Filtro

Puede que sean cargados muchos datos y sea un poco molesto visualizarlos o buscar alguno en especifico, así que sobre el arbol de proyectos hay un input donde por defecto se puede buscar por ID del producto, si necesita buscar por nombre, fecha o costo tiene un menu de opciones a la derecha del input para cambiar de tipo de filtración. Para que funcionen se consutruyeron las funciones validate_is_numeric, validate_is_text, validate_input, filter_treeview y update_treeview.

### Exportaciones

Debajo del arbol de productos y al lado del botón de vender "sell", se encuentran los dos botones con diferentes opciones de exportación: Exportación a csv y exportación a excel. Cuando presione en cualquiera de los dos, el archivo se descargará en su carpeta Descargas de su usuario. Para dar esta funcionalidad se usó la librería pandas dentro de las funciones export_to_excel y export_to_csv.

## Validaciones

La app viene con validaciones para ciertas acciones:
Al momento de registrar un producto, se valida el contenido de los campos con regex para revisar si son validos. Puede ver los patrones dentro de las funciones validate_name y validate_cost.
Cuando se estén filtrando los productos, el menú y el input tendrán validaciones para saber exactamente a que tipo de filtro está estableciendo, validando también si el valor es numérico o texto. Puede ver su funcionamiento dentro de las funciones validate_is_numeric, validate_is_text, validate_input y filter_treeview.

## Manejo de datos

Para manipular los datos que quiera, tiene diferentes

### funciones:

Comprar un producto: De acá salen las validaciones anteriormente nombradas, la fecha de compra se almacena sola mediante el uso de datetime y el ID es autoincremental, así que no hace falta especificarlo en el formulario. Dentro de la app solo bastará con colocar el "Nombre" del producto y el "Costo" del mismo. El funcionamiento puede encontrarlo en las funciones create_element y buy.

### Vender un producto:

Se puede vender un producto haciendo click sobre el que quiera y presionando el boton "sell" que está por debajo del arbol de productos. La idea es que se guarden los datos de la ventas además de los de compra, pero por el momento se está usando una sola tabla. El funcionamiento se encuentra en la función delete_element.

### Edición de productos:

Edite cada producto haciendo doble click sobre el mismo, le apareceran unos campós pequeños con la información del nombre y del costo del producto, puede retirar la acción o terminarla haciendo click sobre cualquiera de los campos y presionando la tecla "enter". Sus funciones son edit_element y save_edit.

# Empezar con el proyecto

Para correr la aplicación por primera vez, necesita crear su entorno virtual, ya sea con anaconda, virutualenvwrapper o los entornos virtuales de python.

### virtualenvwrapper:

`mkvirtualenv mi_env`

### Anaconda:

para anaconda puede usar anaconda navigator o la terminal si lo tiene en las variables de entorno, con la segunda opción sería:
`conda create --name mi_env python=3.11.10`

#### para activarlo:

`conda activate mi_env`

### entornos virtuales de python (venv):

`python -m venv mi_env`

#### para activarlo en windows:

`mi_env/Source/activate`

#### para activarlo en linux o Mac:

`source mi_env/bin/activate`

### Seguido de haber creado y activado su entorno, debe correr el comando `pip install -r requirements.txt` haciendo referencia al archivo que contiene las dependencias del proyecto. Después de eso puede correr main.py y la app va a funcionar perfecto!
