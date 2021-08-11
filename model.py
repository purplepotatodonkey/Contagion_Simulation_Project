"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "Joseph Wang"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)
    
    def distance(self, other: Point) -> float:
        """Finds the distance between two points."""
        x_squared: float = (self.x - other.x) * (self.x - other.x)
        y_squared: float = (self.y - other.y) * (self.y - other.y)
        total: float = x_squared + y_squared
        distance: float = sqrt(total)
        return distance


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.

    def tick(self) -> None:
        """Increases the stimulation by one step."""
        self.location = self.location.add(self.direction)
        if self.sickness >= 90:
            self.immunize()
        if self.is_infected():
            self.sickness += 1

    def contract_disease(self) -> None:
        """Sets the sickness to the diseased value."""
        self.sickness = constants.INFECTED
    
    def immunize(self) -> None:
        """Sets the sickness to the immune value."""
        self.sickness = constants.IMMUNE

    def is_vulnerable(self) -> bool:
        """Sets the sickness to the vulnerable value."""
        return self.sickness == constants.VULNERABLE

    def is_infected(self) -> bool:
        """Sets the sickness to the infected value."""
        return self.sickness >= constants.INFECTED

    def is_immune(self) -> bool:
        """Sets the sickness to the immune value."""
        return self.sickness == constants.IMMUNE

    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable():
            return "gray"
        elif self.is_immune():
            return "green"
        else:
            return "red"
    
    def contact_with(self, other: Cell) -> None:
        """Tests if two cells are in contact."""
        if (self.is_vulnerable() and other.is_infected()) or (self.is_infected() and other.is_vulnerable()):
            self.contract_disease()
            other.contract_disease()


class Model:
    """The state of the simulation."""
    population: List[Cell]
    time: int = 0
    initial_infections: int

    def __init__(self, cells: int, speed: float, initial_infections: int, initial_immunities: int = 0):
        """Initialize the cells with random locations and directions."""
        self.initial_infections = initial_infections
        self.initial_immunities = initial_immunities

        if initial_infections <= 0:
            raise ValueError("We don't have enough infected potatoes.")

        if initial_immunities < 0:
            raise ValueError("Can't have negative potatoes!")

        if (initial_infections + initial_immunities) >= cells:
            raise ValueError("Too few vulnerable potatoes!")
        
        self.population = []
        for _ in range(0, cells):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        
        for i in range(0, initial_infections):
            self.population[i].contract_disease()
        
        for j in range(initial_infections, initial_infections + initial_immunities):
            self.population[j].immunize()
        
    def check_contacts(self) -> None:
        """Checks every cell in the population for contacts."""
        point_one: Point = Point(0, 0)
        point_two: Point = Point(0, 0)

        for cell_one in range(0, len(self.population)):
            # print("cell_one:")
            # print(cell_one)
            # print(self.population[cell_one])
            # print(self.population[cell_one].is_vulnerable)
            for cell_two in range(cell_one + 1, len(self.population)):
                # print("cell_two:")
                # print(cell_two)
                # print(self.population[cell_two])
                # print("distance:")
                # print(self.population[cell_one].location.distance(self.population[cell_two].location))
                point_one = self.population[cell_one].location
                point_two = self.population[cell_two].location
                check_distance = point_one.distance(point_two)
                if check_distance <= constants.CELL_RADIUS:
                    self.population[cell_one].contact_with(self.population[cell_two])
    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        """Tests if the model has completed."""
        complete_bool: bool = True
        for cell in self.population:
            if cell.is_infected():
                complete_bool = False
        return complete_bool