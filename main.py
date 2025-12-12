import math
import itertools
import sys

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
class Point:
    def __init__(self, x, y):
        """Create a point with numeric coordinates (converted to float)."""
        try:
            self.x = float(x)
            self.y = float(y)
        except ValueError:
            raise ValueError("Point coordinates must be numeric.")
        self.coords = (self.x, self.y)

    def calc_distance(self, other_point):
        """Return Euclidean distance to another Point."""
        return math.sqrt((self.x - other_point.x) ** 2 +(self.y - other_point.y) ** 2)

    def __repr__(self):
        """Return a string representation of the point."""
        return f"({self.x}, {self.y})"


class PathFinder:
    def __init__(self, points_array_raw):
        """Prepare the start point and the list of points to visit."""
        self.points_array = points_array_raw
        self.start_point = Point(0, 0)
        self.points_to_visit = [
            p for p in self.points_array
            if p.coords != self.start_point.coords
        ]

    def find_shortest_path(self):
        """
        Compute the shortest path starting and ending at (0,0),
        visiting all given points exactly once.
        Returns:
            (best_path, total_distance - string format)
        """
        if not self.points_to_visit:
            return [self.start_point], 0

        min_distance = sys.maxsize
        shortest_path = []

        # Try all permutations (brute-force TSP)
        for path_perm in itertools.permutations(self.points_to_visit):
            path = [self.start_point] + list(path_perm) + [self.start_point]
            dist = 0

            # Sum distances along the current path
            for p_from, p_to in zip(path, path[1:]):
                dist += p_from.calc_distance(p_to)

            # Keep best path found
            if dist < min_distance:
                min_distance = dist
                shortest_path = path
        return shortest_path, f"{min_distance:.3f}"

@app.errorhandler(404)
def invalid_route(e):
    """ Not existed url - redirect to homepage"""
    print(f"Invalid Input Error (Redirect Triggered): {e}", file=sys.stderr)
    return redirect("http://127.0.0.1:5000/")


def parse_points(location_string: str):
    """
    Parse the 'locations' string into a list of Point objects.
    Keeps the same validation messages as in the original code.
    Raises ValueError with the appropriate message if input is invalid.
    """
    if not location_string or not location_string.strip():
        raise ValueError("must enter valid points with [(,),...,(,)] form")
    if " " in location_string:
        raise ValueError("must enter valid points with [(,),...,(,)] form")

    # Expecting a string like: [(1,1),(-1,-1),(2,3)]
    try:
        arr = eval(location_string, {"__builtins__": None}, {})
    except Exception:
        raise ValueError("must enter valid points with [(,),...,(,)] form")

    if not arr:
        raise ValueError("must enter points with integer or float value")

    if not isinstance(arr, list):
        raise ValueError("input must be a list of tuples")
    points = []
    for item in arr:
        if not isinstance(item, (tuple)) or len(item) != 2:
            raise ValueError("must enter valid points with [(,),...,(,)] form")
        x, y = item
        p = Point(x, y)  # Point itself checks that coordinates are integers
        points.append(p)
    return points

@app.route('/')
def main_page():
    """
      Home page:
      - Reads 'locations' from the query string.
      - Validates and parses it to Point objects.
      - On valid input computes and displays the shortest path.
      - On error or missing input shows home page with an error message.
      """
    location_string = request.args.get('locations')
    error_message = None
    if location_string:
        try:
            points = parse_points(location_string)
            solver = PathFinder(points)
            path, length = solver.find_shortest_path()
            return render_template("results.html", path=path, leng=length)
        except (ValueError, AttributeError, IndexError) as e:
            error_message = f" error {e}"
            print(f"Input processing error: {error_message}", file=sys.stderr)
    return render_template('home_page.html', error_message=error_message)


# location_string = request.args.get('locations') #מקבל את הנתונים שהתקבלו מהURL
# error_message = None #משתנה לאיכסון הודעת שגיאה
# if location_string:
#     try:# בדיקת תקינות שהמחרוזת אינה ריקה לאחר ה =locations?/
#         if not location_string.strip():
#             error_message = "must enter valid points with [(,),...,(,)] form"
#         if error_message is None: #אם אין שגיאות
#             # בדיקת תקינות של ניתוח מחרוזת
#             location_string_new = location_string.removeprefix('[(').removesuffix(')]')#מוריד שני תווים מהקצוות
#             if not location_string_new.strip(): #בדיקה שלא ריק
#                 error_message = "must enter points with integer value"
#             if error_message is None:#אם אין שגיאות
#                 locations_parts = location_string_new.split('),(')#מקבלים מערך של זוגות מספרים המופרדים על ידי , מסוג סטרינג
#                 points = [] #מערך ריק שנמלא בנקודות
#                 for part in locations_parts:
#                     point_coords = part.split(',') #נקבל מערך שח זוגות מספרים
#                     # בדיקת תקינות שמקבלים 2 קאורדינטות בלבד
#                     if len(point_coords) != 2:
#                         error_message = "must enter points with 2 cordinates"
#                         raise ValueError( "must enter points with 2 cordinates")
#                     p = Point(point_coords[0].strip(), point_coords[1].strip()) #יצירת אובייקט Point לכל סוג מספרים ומוריד רווחים סביב המספרים
#                     points.append(p) #מוסיף את הנקודה מסוג Point למערך נקודות
#                 shortest_path = PathFinder(points) #אובייקט מסוג PathFinder המקבל את מערך הנקודות שבנינו
#                 shortest_path_new = shortest_path.find_shortest_path() #מריץ את הפעולה למצוא את הדרך הקצרה ביותר ומקבל במקום [0] את הרשימה לפי סדר הנקודות וב[1] את האורך של המסלול
#                 return render_template("results.html", path=shortest_path_new[0], leng=shortest_path_new[1])
#
#     except (ValueError, AttributeError, IndexError) as e:
#         # הודעת שגיאה
#         error_message = f" error {e}"
#         print(f"Input processing error: {error_message}", file=sys.stderr)

# return render_template('home_page.html', error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)