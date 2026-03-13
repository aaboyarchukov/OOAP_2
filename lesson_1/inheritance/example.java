public interface Shape {
	double area();
	double perimeter();
}

public record Point(double x, double y) {
	// ...
}

public class Ellipse implements Shape {
	private Point f1; // composition
	private Point f2; // composition
	
	@Override
	public double area() {
		//...
	}
	
	@Override
	public double perimeter() {
		//...
	}
}

public class Circle extends Ellipse {
	private Point center;
    private double radius;
	
	@Override
	public double area() {
		//...
	}
	
	@Override
	public double perimeter() {
		//...
	}
}