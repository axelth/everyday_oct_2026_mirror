import can_i_see_that_path.path_tools as pt

from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib import parse

class RequestHandler(BaseHTTPRequestHandler):
    content_type = "text/html; charset=utf-8"
    
    def do_GET(self):
        parts = [self.make_html_header("Request")]
        parts.append("""<form action="submit" method="POST">
          <input type="text" name="path" placeholder="Enter path to test">
          <button type="submit">Check path</button>
        </form>""")
        parts.append(self.close_html())

        resp_data = "\n".join(parts).encode("utf8")
        
        self.send_response(200)
        self.send_header("Content-Type", self.content_type)
        self.end_headers()

        self.wfile.write(resp_data)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf8').strip()
        post_dict = parse.parse_qs(post_data)
        print(post_dict)
        path = post_dict.get("path", [None])
        path = path[0]
        if path is None :
            status_code = 400
            resp_data = f"No path posted\r\n\r\n".encode('utf8')            
        if not pt.validate_path(path):
            status_code = 400
            resp_data = f"Path '{path}' is not a valid path\r\n\r\n".encode('utf8')
        else:
            try:
                can_access, message_parts, dir_listing = pt.check_path_access(path)
                status_code = 200
                resp_data = self.make_post_response_html(can_access, message_parts, dir_listing)
            except Exception as e: 
                print(e)
                status_code = 500
                resp_data = b"An exception occurred"
                raise

        self.send_response(status_code)
        self.send_header("Content-Type", self.content_type)
        self.end_headers()

        self.wfile.write(resp_data)

        

    def make_post_response_html(self, can_access: bool, message_parts: list[str], directory_listing: None|list[str]) -> bytes:
        parts = [self.make_html_header("Result")]
        parts.append(self.banner(can_access))
        if len(message_parts) > 1:
            # wrap message parts except for the stat result in a p tag
            parts.extend(self.paragraph_wrap(message_parts[:-1]))
        
        parts.append(self.pre_wrap(message_parts[-1]))

        if directory_listing:
            parts.append(self.ul_wrap(directory_listing))
        
        parts.append(self.close_html())

        return '\n'.join(parts).encode("utf8")


    def make_html_header(self, title: str) -> str:
        return f"""<html>
            <head>
              <title>{title}</title>
        <style>
        pre {{
          background-color: black;
          color: white;
          padding: 5px;
        }}
        </style>
        <head>
        <body>
        """
    def paragraph_wrap(self, message_parts: list[str]) -> list[str]:
        return [f'<p>{part}</p>' for part in message_parts]

    def pre_wrap(self, pre_text: str) -> str:
        return f'<pre>{pre_text}</pre>'
    
    def close_html(self) -> str:
        return "</body>\n</html>"

    def banner(self, yes: bool) -> str:
        banner_class, banner_text = ("yes", "YES") if yes else ("no", "NO")
        return f'<div class="{banner_class}"><p>{banner_text}</p></div>'

    def ul_wrap(self, items: list[str]) -> str:
        li_items_str = '\n'.join([f'\t<li>{item}</li>' for item in items])
        return f'<ul>\n{li_items_str}\n</ul>'


def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Serving ", repr(httpd))
    httpd.serve_forever()
