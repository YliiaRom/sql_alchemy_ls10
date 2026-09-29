from livereload import Server

server = Server()

server.watch("static/styles.css")
server.watch("templates")

server.serve(
    root=".",
    port=5500,
)