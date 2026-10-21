import nox


def _install_dev_deps(session):
    session.install("-e", ".")
    session.install(
        "pytest>=8.0",
        "pytest-cov>=5.0",
        "ruff>=0.5",
        "mypy>=1.10",
        "nox>=2024.3",
        "pre-commit>=3.7",
        "mkdocs>=1.6",
    )


@nox.session
def tests(session):
    _install_dev_deps(session)
    session.run("pytest", "-q")


@nox.session
def lint(session):
    _install_dev_deps(session)
    session.run("ruff", "check", ".")


@nox.session
def types(session):
    _install_dev_deps(session)
    session.run("mypy", "src")


@nox.session
def docs(session):
    _install_dev_deps(session)
    session.run("mkdocs", "build", "--strict")
