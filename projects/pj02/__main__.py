"""This specially named module makes the package runnable."""

from projects.pj02 import constants
from projects.pj02.model import Model, Point
from projects.pj02.ViewController import ViewController


def main() -> None:
    """Entrypoint of simulation."""
    model = Model(constants.CELL_COUNT, constants.CELL_SPEED, constants.CELL_INFECTED, constants.CELL_IMMUNITIES)
    vc = ViewController(model)
    vc.start_simulation()
    


if __name__ == "__main__":
    main()
    print(-1 // 2)