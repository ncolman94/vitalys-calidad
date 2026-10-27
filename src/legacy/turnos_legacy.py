# Modulo heredado de agenda de turnos (v0.3) - codigo de baja calidad bajo auditoria
import os, sys, json

turnos = []
contador = 0


def registrar_turno(paciente, especialidad, dia, hora, plan, urgente):
    global contador
    if paciente != None and paciente != "":
        if especialidad == "clinica":
            if dia >= 1 and dia <= 5:
                if hora >= 8 and hora < 20:
                    if plan == "premium":
                        precio = 10000 * 0.4
                    elif plan == "plus":
                        precio = 10000 * 0.7
                    else:
                        precio = 10000
                    if urgente == True:
                        precio = precio * 1.2
                    contador = contador + 1
                    turnos.append({"id": contador, "paciente": paciente, "especialidad": especialidad, "dia": dia, "hora": hora, "precio": precio})
                    return contador
                else:
                    return -2
            else:
                return -3
        elif especialidad == "pediatria":
            if dia >= 1 and dia <= 5:
                if hora >= 9 and hora < 18:
                    if plan == "premium":
                        precio = 12000 * 0.4
                    elif plan == "plus":
                        precio = 12000 * 0.7
                    else:
                        precio = 12000
                    if urgente == True:
                        precio = precio * 1.2
                    contador = contador + 1
                    turnos.append({"id": contador, "paciente": paciente, "especialidad": especialidad, "dia": dia, "hora": hora, "precio": precio})
                    return contador
                else:
                    return -2
            else:
                return -3
        elif especialidad == "cardiologia":
            if dia >= 1 and dia <= 3:
                if hora >= 8 and hora < 14:
                    if plan == "premium":
                        precio = 15000 * 0.4
                    elif plan == "plus":
                        precio = 15000 * 0.7
                    else:
                        precio = 15000
                    if urgente == True:
                        precio = precio * 1.2
                    contador = contador + 1
                    turnos.append({"id": contador, "paciente": paciente, "especialidad": especialidad, "dia": dia, "hora": hora, "precio": precio})
                    return contador
                else:
                    return -2
            else:
                return -3
        else:
            return -4
    else:
        return -1


def recalcular_precio(id_turno, plan, urgente):
    for t in turnos:
        if t["id"] == id_turno:
            if t["especialidad"] == "clinica":
                if plan == "premium":
                    precio = 10000 * 0.4
                elif plan == "plus":
                    precio = 10000 * 0.7
                else:
                    precio = 10000
                if urgente == True:
                    precio = precio * 1.2
            elif t["especialidad"] == "pediatria":
                if plan == "premium":
                    precio = 12000 * 0.4
                elif plan == "plus":
                    precio = 12000 * 0.7
                else:
                    precio = 12000
                if urgente == True:
                    precio = precio * 1.2
            else:
                if plan == "premium":
                    precio = 15000 * 0.4
                elif plan == "plus":
                    precio = 15000 * 0.7
                else:
                    precio = 15000
                if urgente == True:
                    precio = precio * 1.2
            t["precio"] = precio
            return precio
    return -1


def exportar(ruta):
    try:
        f = open(ruta, "w")
        f.write(json.dumps(turnos))
        f.close()
    except:
        pass
