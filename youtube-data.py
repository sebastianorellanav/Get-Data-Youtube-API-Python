from googleapiclient.discovery import build
from oauth2client.tools import argparser
import json

api_key = 'AIzaSyBEG4VNPxdD299X5H_bPdp6twfAUIAhcjo'
youtube = build('youtube', 'v3', developerKey = api_key)
search_querys = ["api rest python", 
                "python numpy", 
                "python libreria requests", 
                "python tkinter", 
                "python pyqt", 
                "python pandas",
                "curso de python", 
                "python",
                "java POO",
                "java herencia",
                "java interfaces",
                "java clases",
                "java sobrescritura",
                "java api rest",
                "java spring",  
                "java servidor",
                "java",
                "punteros en c",
                "programar en c",
                "estructuras en c",
                "algoritmo ordenamiento en c",
                "algoritmo en c",
                "lista enlazada en c",
                "array en c",
                "lenguaje programacion c"]

    
def getComentarios(video_id, maxPages):
    print("                     Obteniendo Comentarios\n")
    comentarios = []
    # retrieve youtube video results
    response=youtube.commentThreads().list(
    part='snippet',
    videoId=video_id
    ).execute()

    i = 0
    while i < maxPages:
        #print("pagina de comentarios n° "+str(i))
        for item in response['items']:
            contenido = item['snippet']['topLevelComment']['snippet']['textDisplay']
            autor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            likes = item['snippet']['topLevelComment']['snippet']['likeCount']
            comentario = {'autor':autor, 'contenido': contenido, 'likes': likes}
            comentarios.append(comentario)

        if 'nextPageToken' in response and i < maxPages:
            nextPageToken = response['nextPageToken']
            response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                    pageToken=nextPageToken
                ).execute()
        else:
            break
        i+=1
    
    return comentarios

def getLikesAndDescription(video_id):
    print("                 Obteniendo comentarios, likes y tags ")
    response = youtube.videos().list(
        part='snippet, statistics',
        id=video_id
    ).execute()

    descripcion = response['items'][0]['snippet']['description']
    
    if 'likeCount' in response['items'][0]['statistics']:
        likes = response['items'][0]['statistics']['likeCount']
    else:
        likes = 0

    if 'tags' in response['items'][0]['snippet']:
        tags = response['items'][0]['snippet']['tags']
    else:
        tags = []

    #if response['items'][0]['statistics']['commentCount'] != 0:
    try:
        comentarios = getComentarios(video_id, 1)
    except:
        print("Los comentarios de este video estan desactivados")
        comentarios = []

    return [descripcion, likes, tags, comentarios]

def getVideos(query, maxPages):
    print("         Obteniendo videos")
    videos = []
    #argparser.add_argument("--q", help="Search term", default=query)
    #argparser.add_argument("--max-results", help="Max results", default=25)
    #args = argparser.parse_args()


    response = youtube.search().list(
            q= query,
            part='snippet',
            type='video',
            maxResults=15
    ).execute()

    i = 0
    while i < maxPages:
        #print("pagina de videos n° "+str(i))
        for item in response.get("items", []):
            videoId = item['id']['videoId']
            print("             Video: "+str(videoId))
            url = "https://www.youtube.com/watch?v="+str(item['id']['videoId'])
            title = item['snippet']['title']
            channelTitle = item['snippet']['channelTitle']
            publishedAt = item['snippet']['publishedAt'][:10]

            masInfo = getLikesAndDescription(videoId)
            description = masInfo[0]
            likes = masInfo[1]
            tags = masInfo[2]
            comentarios = masInfo[3]

            video = {'id':videoId, 
                    'url':url, 
                    'titulo':title, 
                    'descripcion':description, 
                    'tags':tags,
                    'autor':channelTitle, 
                    'fecha':publishedAt,
                    'likes':likes,
                    'comentarios':comentarios}
            videos.append(video)

        if 'nextPageToken' in response and i < maxPages:
            nextPageToken = response['nextPageToken']
            response = youtube.search().list(
                    q= query,
                    part='snippet',
                    type='video',
                    pageToken=nextPageToken
                    ).execute()
        else:
            break
        i+=1
    
    return videos


#################################################################################################
################################## main #########################################################
print("Conectando con la API de Youtube...\n")
#Crear archivo
f = open ('example.json','w')      ### OMITIR ESTA PARTE PARA AGREGAR MAS VIDEOS
f.write('[')
f.close()

# Realizar las querys a youtube
for query in search_querys:
    print("     Buscando videos de: '"+query+"'")
    videos = getVideos(query, 1)
    
    #Guardar los resultados en el archivo
    print("     Escribiendo en archivo .json")
    f = open("prueba2.json", "a")
    for e in videos:
        json.dump(e,f)
        f.write(',')
    
    print("\n")


# Cerrar youtube y archivo
youtube.close()
f.write(']')
f.close()









