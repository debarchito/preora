import nox


@nox.session(name="simple_test", venv_backend="none")
def tests(session):
    session.run("pytest")
