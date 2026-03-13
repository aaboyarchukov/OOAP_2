public interface Shape {
    double area();

    double perimeter();
}

public record Point(double x, double y){
// ...
}

public class Ellipse implements Shape {
    private Point f1; // composition
    private Point f2; // composition

    @Override
    public double area() {
        // ...
    }

    @Override
    public double perimeter() {
        // ...
    }
}

public class Circle extends Ellipse {
    private Point center;
    private double radius;

    @Override
    public double area() {
        // ...
    }

    @Override
    public double perimeter() {
        // ...
    }

}

    public double GetArea(ellipse Ellipse) {
        return ellipse.area();
    }

    // или

public double GetArea(shape Shape) {
	return shape.area();
}

GetArea(new Circle(...))
GetArea(new Ellipse(...))
