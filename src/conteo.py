
class Contador:
    def __init__(self):
        self.multiplicaciones = 0
        self.divisiones = 0
        self.sumas = 0
        self.restas = 0
        self.comparaciones = 0
        self.comparaciones_escalas = 0
        self.intercambios = 0
        self.pasos = []

    def nuevo_paso(self):
        paso = {
            "multiplicaciones": 0,
            "divisiones": 0,
            "sumas": 0,
            "restas": 0
        }
        self.pasos.append(paso)

    def registrar(self, operacion):
        if operacion == "multiplicacion":
            self.multiplicaciones += 1
            self.pasos[-1]["multiplicaciones"] += 1

        elif operacion == "division":
            self.divisiones += 1
            self.pasos[-1]["divisiones"] += 1

        elif operacion == "suma":
            self.sumas += 1
            self.pasos[-1]["sumas"] += 1

        elif operacion == "resta":
            self.restas += 1
            self.pasos[-1]["restas"] += 1

    def contar_comparacion(self):
        self.comparaciones += 1

    def contar_intercambio(self):
        self.intercambios += 1

    def total_flops(self):
        return (
            self.multiplicaciones
            + self.divisiones
            + self.sumas
            + self.restas
        )

    def mostrar_resumen(self):
        print("Multiplicaciones:", self.multiplicaciones)
        print("Divisiones:", self.divisiones)
        print("Sumas:", self.sumas)
        print("Restas:", self.restas)
        print("Total de flops:", self.total_flops())
        print("Comparaciones:", self.comparaciones)
        print("Intercambios:", self.intercambios)
