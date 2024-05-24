import requests


if __name__ == "__main__":
    url = 'https://httpbin.org/get?nombre=adrian&curso=python'
    args = {'nombre':'Adrian', 'Curso':'python', 'nivel':'Intermedio'}

    response = requests.get(url, params= args)
    print(response.url)

    if response.status_code == 200:
        response_json = response.json()
        args = response_json['args']
        print(args)