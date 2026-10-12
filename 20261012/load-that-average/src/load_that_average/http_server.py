import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from load_that_average.db_wrapper import DbReader

class RequestHandler(BaseHTTPRequestHandler):
    db_reader = None
    content_type = "text/html; charset=utf-8"
    
    def __init__(self, db_path, *args, **kwargs):
        self.db_reader = DbReader(db_path)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        load_averages = reversed(self.db_reader.get_latest_load_averages())

        resp_data = self.make_response_html(load_averages)
        self.send_response(200)
        self.send_header("Content-Type", self.content_type)
        self.end_headers()

        self.wfile.write(resp_data)

        

    def make_response_html(self, load_averages: list[tuple]) -> bytes:
        parts = [self.make_html_header("Result")]
        parts.extend(self.paragraph_wrap(["The thirty latest load averages recorded on the system"]))
        parts.append(self.make_table_header())
        parts.extend([self.load_avg_table_row(*r) for r in load_averages])
        parts.append(self.close_table())
        parts.append(self.close_html())
        # print(parts)
        return ('\n'.join(parts)).encode("utf8")


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
    def make_table_header(self) -> str:
        return """
        <table>
        <thead>
          <tr><th>time</th><th>1 min avg</th><th>5 min avg</th><th>15 min avg</th></tr>
        </thead>
        <tbody>"""

    def close_table(self) -> str:
        return """</tbody>
        </table>"""

    def load_avg_table_row(self, timestamp, one_min, five_min, fifteen_min) -> str:
        time_str = time.strftime("%y%d%m %H:%M:%S", time.localtime(timestamp))
        load_strs = [f"{l:.4f}" for l in (one_min, five_min, fifteen_min)]
        td_strs = [f"<td>{val}</td>" for val in [time_str, *load_strs]]
        return f"<tr>{''.join(td_strs)}</tr>"
        
    def paragraph_wrap(self, message_parts: list[str]) -> list[str]:
        return [f'<p>{part}</p>' for part in message_parts]

    def pre_wrap(self, pre_text: str) -> str:
        return f'<pre>{pre_text}</pre>'
    
    def close_html(self) -> str:
        return "</body>\n</html>"
