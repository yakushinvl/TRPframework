from django.http import HttpResponse


def page(title, content):
    bootstrap = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">учёт выступлений</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">главная</a>
                <a class="nav-link" href="/presentations/">выступления</a>
                <a class="nav-link" href="/events/">мероприятия</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5 fw-bold">сервис учёта выступлений студентов</h1>
        <p class="lead">система регистрации, учёта и оценивания докладов на научных мероприятиях</p>
        <hr class="my-4">
        <p>выбери нужный раздел:</p>
        <a href="/presentations/" class="btn btn-primary me-2">список выступлений</a>
        <a href="/events/" class="btn btn-outline-secondary">мероприятия</a>
    </div>
    """
    return HttpResponse(page("главная – учёт выступлений", content))


def page_not_found(request, exception):
    content = """
    <div class="text-center py-5">
        <h1 class="display-4 text-danger">404 – страница не найдена</h1>
        <p class="lead">запрошенная страница не существует</p>
        <a href="/" class="btn btn-primary">вернись на главную</a>
    </div>
    """
    return HttpResponse(page("404 – страница не найдена", content), status=404)
