 #Uso del api Imagekit, Imagga y acceso a BBDD

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import base64
import requests
import os
import pymysql
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() 

IMAGEKIT_PUBLIC_KEY=os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY=os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_ENDPOINT=os.getenv("IMAGEKIT_PRIVATE_KEY")

IMAGGA_API_KEY=os.getenv("IMAGGA_API_KEY")
IMAGGA_API_SECRET= os.getenv("IMAGGA_API_SECRET")

MY_SQL_HOST=os.getenv("MY_SQL_HOST")
MY_SQL_USER=os.getenv("MY_SQL_USER")
MY_SQL_PASSWORD=os.getenv("MY_SQL_PASSWORD")

IMAGES_OS_PATH="Imagenes"

RUTA_IMAGENES=os.path.join(os.getcwd(),IMAGES_OS_PATH)

#######################
########UTILIDADES#####
#######################

# def get_image_from_url(url):
#     response = requests.get(url)
#     fichero=url.rsplit('/', 1)[-1]
#     if response.status_code == 200:
#         print("Imagen de Url obtenida OK")
#         ruta_fichero=os.path.join(RUTA_IMAGENES,fichero)
#         #"{os.getcwd()}/{fichero}"
#         with open(ruta_fichero, 'wb') as f:
#             f.write(response.content)
#         with open(ruta_fichero, mode="rb") as img:
#             imgstr = base64.b64encode(img.read())
#     if os.path.exists(ruta_fichero):
#         os.remove(ruta_fichero)
    
#     return imgstr

def save_image_to_os(image,imagenb64):

    """Descarga el contenido de una imagen en una url y crea un archivo en el sistema operativo"""
    nombre_imagen=f"{image.file_id}_{image.name}"
    ruta_imagen=os.path.join(RUTA_IMAGENES,nombre_imagen)
    print(f"Imagen a guardar en /app/Imagenes: {ruta_imagen}")
    imgb64decode = base64.b64decode(imagenb64)

    with open(ruta_imagen, 'wb') as f:
        f.write(imgb64decode)


def get_file_size(image):
    """Obtiene el tamaño de una imagen almacenada en imagenes"""
    size=os.path.getsize(image)
    return size


#######################
########IMAGEKIT#######
#######################

imagekit = ImageKit(
    public_key=IMAGEKIT_PUBLIC_KEY,
    private_key=IMAGEKIT_PRIVATE_KEY,
    url_endpoint = IMAGEKIT_ENDPOINT
)

def upload_image(url,image_name):
    """Subida de imágenes a Imagekit"""
    options_upload = UploadFileRequestOptions(use_unique_file_name=True) #desactivamos que se genere un código al final de la imagen

    upload_image=imagekit.upload(file=url, file_name=image_name,options=options_upload)

    print("Image subida correctamente")
    return upload_image


def list_images():
    """Devuelve el listado de imagenes almacenadas en Imagekit"""
    print("LISTADO DE IMAGENES")
    print("-------------------------------")
    images = imagekit.list_files()
    for i in images.list:
        print(f"id={i.file_id}, name={i.name}, url={i.url}, tags={i.tags}")


def delete_image(id):
    """Borra una imagen de Imagekit"""
    try:
        imagekit.delete_file(file_id=id)
        print(f"Borrado imagen con id={id} OK")
    except:
        print(f"La imagen con id {id} no existe")



######################
#########IMAGGA#######
######################

def get_tags_imagga(img_url,min_confidence,IMAGGA_API_KEY,IMAGGA_API_SECRET):
    """Obtiene los tags de una imagen atacando al API de Imagga"""

    response = requests.get(f"https://api.imagga.com/v2/tags?image_url={img_url}", auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET))
    min_confidence=10
    tags = [
        {
            "tag": t["tag"]["en"],
            "confidence": t["confidence"]
        }
        for t in response.json()["result"]["tags"]
        if t["confidence"] > min_confidence
    ]

    return tags



###############################
################BBDD###########
###############################

def create_tables():
    """Creación de tablas BBDD Pictures"""
    connection = pymysql.connect(
                             host=MY_SQL_HOST,
                             user=MY_SQL_USER,
                             password=MY_SQL_PASSWORD,
                             database='Pictures',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

    with connection.cursor() as cur:
            cur.execute("""
               CREATE TABLE pictures(
                    id VARCHAR(36),
                    path VARCHAR(300),
                    created_at TIMESTAMP,
                    PRIMARY KEY(id)
                )
                """)
            cur.execute("""
                CREATE TABLE tags(
                    tag VARCHAR(32),
                    picture_id VARCHAR(100),
                    confidence FLOAT(15,13),
                    created_at TIMESTAMP,
                    PRIMARY KEY(tag,picture_id),
                    FOREIGN KEY (picture_id)
                        REFERENCES pictures(id)
                )
                """)


def truncate_tables():
    connection = pymysql.connect(
                             host=MY_SQL_HOST,
                             user=MY_SQL_USER,
                             password=MY_SQL_PASSWORD,
                             database='Pictures',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)
    

    
    with connection.cursor() as cur:
            cur.execute(f"""SET FOREIGN_KEY_CHECKS = 0""")
            cur.execute(f"""TRUNCATE TABLE tags""")
            cur.execute(f"""TRUNCATE TABLE pictures""")
            cur.execute(f"""SET FOREIGN_KEY_CHECKS = 1""")

    print(f"Truncado tablas OK")

def drop_tables():
    """Borrado de tablas BBDD Pictures"""
    connection = pymysql.connect(
                             host=MY_SQL_HOST,
                             user=MY_SQL_USER,
                             password=MY_SQL_PASSWORD,
                             database='Pictures',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)
    with connection.cursor() as cur:
            cur.execute(f"""DROP TABLE tags""")          
            cur.execute(f"""DROP TABLE pictures""")
    print("Drop tables OK")       


def insert_image_bbdd(image,list_tags):
     
    connection = pymysql.connect(
                             host=MY_SQL_HOST,
                             user=MY_SQL_USER,
                             password=MY_SQL_PASSWORD,
                             database='Pictures',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)
    
    nombre_imagen=f"{image.file_id}_{image.name}"
    ruta_imagen=os.path.join(RUTA_IMAGENES,nombre_imagen)

    created_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    with connection.cursor() as cursor:
        # Insercción en pictures
        sql = "INSERT INTO `pictures` (`id`, `path`, `created_at`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (image.file_id,ruta_imagen, created_at))
    print("Insercción en tabla pictures OK")

    with connection.cursor() as cursor: 
        #Insercción en tags
        sql = "INSERT INTO `tags` (`tag`, `picture_id`, `confidence`, `created_at`) VALUES (%s, %s, %s, %s)"
        cursor.executemany(sql,list_tags)
    print("Insercción en tabla tags OK")


def execute_sql(sql,*args):
    connection = pymysql.connect(
                             host=MY_SQL_HOST,
                             user=MY_SQL_USER,
                             password=MY_SQL_PASSWORD,
                             database='Pictures',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)


    print(f"args: {args}")
    print(f"SQL a ejecutar: {sql}")
    if args == ():
        print("Entra en IF")
        try:
            with connection.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        except Exception as e:
            print(f"Por favor introduzca una sql válida: {e}")  
    else:
        print(f"SQL a ejecutar: {sql}")

        try:
            print(f"ARGS: {args[0]})")
            with connection.cursor() as cur:
                cur.execute(sql,args[0])
                return cur.fetchall()
        except:
            print("Por favor introduzca una sql válida")

        


###########################################################
###METODOS APP (post_image, get_images, get_image....)#####
###########################################################

def post_image(**kwargs):
    """Combina distintas funciones para cubrir las funcionalidades del API"""

    url=kwargs['url']
    imagenb64=kwargs['imagenb64']
    image_name=kwargs['image_name']


    #Subida de Imagen en Imagekit
    imagen=upload_image(imagenb64,image_name)
    imagen_id=imagen.file_id
    print(f"Subida Correcta a IMAGEKIT de imagen {imagen.name} con id={imagen.file_id}")

    #Obtención de Tags
    imagen_tags=get_tags_imagga(url,10,IMAGGA_API_KEY,IMAGGA_API_SECRET)
    print(f"Extracción Correcta de tags desde IMAGGA, Total tags:{len(imagen_tags)}")

    #Almacenamiento en BBDD
    created_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    list_tags = list([(x['tag'],imagen.file_id, x['confidence'],created_at) for x in imagen_tags])
    insert_image_bbdd(imagen,list_tags)
    print("Inserción correcta de Imagen y tag en BBDD")

    #Guardado de Imagen en carpeta
    save_image_to_os(imagen,imagenb64)
    print(f"Guardado de Imagen {imagen.name} en carpeta ..{IMAGES_OS_PATH}")

    #Borrado de Imagen en Imagekit
    delete_image(imagen.file_id)
    print(f"Borrado de Imagen {imagen.name} con id={imagen.file_id} de IMAGEKIT")

    resultado={}
    resultado['id']=imagen_id

    return resultado


def get_images(**kwargs):


    print(f"kwargs : {kwargs}")

    if "min_date" in kwargs and "max_date" in kwargs:
        print("Filtros de fecha indicados")
        list=[]
        min_date=datetime.strptime( kwargs['min_date'],'%Y-%m-%d %H:%M:%S')
        max_date=datetime.strptime( kwargs['max_date'],'%Y-%m-%d %H:%M:%S')
        sql="""SELECT * FROM pictures where created_at >= %s and created_at <= %s"""
        list=execute_sql(sql,(min_date,max_date))

    if "min_date" in kwargs and "max_date" not in kwargs:
        print("Filtros de fecha inferior indicado")
        list=[]
        min_date=datetime.strptime( kwargs['min_date'],'%Y-%m-%d %H:%M:%S')
        sql="""SELECT * FROM pictures where created_at >= %s"""
        list=execute_sql(sql,(min_date))
    
    if "min_date" not in kwargs and "max_date"  in kwargs:
        print("Filtros de fecha superior indicado")
        list=[]
        max_date=datetime.strptime( kwargs['max_date'],'%Y-%m-%d %H:%M:%S')
        sql="""SELECT * FROM pictures where created_at <= %s"""
        list=execute_sql(sql,(max_date))

    if  kwargs == {} :
        print("Filtros de fecha no indicados")
        sql="SELECT * FROM pictures"
        list=execute_sql(sql)

    resultado=[]
    for i in list:
        d=dict()
        d['id']=i['id']
        d['size']=get_file_size(i['path'])
        #i['path'].rsplit('/', 1)[-1]
        d['date']=i['created_at'].strftime('%Y-%m-%d %H:%M:%S') 
        #tags
        sql="""SELECT tag,confidence FROM tags where picture_id = %s"""
        list_tags=execute_sql(sql,(i['id']))
        d['tags']=list_tags

        resultado.append(d)
 
    print("Imagenes obtenidas OK")
    return resultado
       
        
def get_image(id):

    sql="SELECT * FROM pictures where id=%s"
    imagen=execute_sql(sql,id)[0]

    print(imagen)

     #tags
    sql="SELECT tag,confidence FROM tags where picture_id=%s"
    list_tags=execute_sql(sql,id)

    d=dict()
    d['id']=imagen['id']
    d['size']=get_file_size(imagen['path'])
    d['date']=imagen['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    d['tags']=list_tags
    d['data']=""
    with open (imagen['path'],'rb') as image_file:
        imagen_encodeb64=base64.b64encode(image_file.read())
        d['data']=imagen_encodeb64.decode()

    return d





