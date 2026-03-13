package polymorphism


type Parrot interface {
	Speed() float32
	Weight() float32
	Сolor() string
}

type AfricanParrot struct {
	Speed float64
	Weight float64
	Color string
}

func (afp *AfricanParrot) Speed() float32 {}
func (afp *AfricanParrot) Weight() float32 {}
func (afp *AfricanParrot) Сolor() float32 {}

type EuropianParrot struct {
	Speed float64
	Weight float64
	Color string
}

func (ep *EuropianParrot) Speed() float32 {}
func (ep *EuropianParrot) Weight() float32 {}
func (ep *EuropianParrot) Сolor() float32 {}

func GetParrotInfo(parrot Parrot) {
	// invoke methods
}

GetParrotInfo(EuropianParrot{...})
GetParrotInfo(AfricanParrot{...})