# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\appointment_update.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpdateAppointmentWindow(object):
    def setupUi(self, UpdateAppointmentWindow):
        UpdateAppointmentWindow.setObjectName("UpdateAppointmentWindow")
        UpdateAppointmentWindow.resize(500, 400)
        self.lb_title = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_title.setGeometry(QtCore.QRect(100, 20, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_title.setObjectName("lb_title")
        self.lb_patient = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_patient.setGeometry(QtCore.QRect(30, 80, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_patient.setFont(font)
        self.lb_patient.setObjectName("lb_patient")
        self.lb_patient_name = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_patient_name.setGeometry(QtCore.QRect(160, 80, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_patient_name.setFont(font)
        self.lb_patient_name.setObjectName("lb_patient_name")
        self.lb_date = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_date.setGeometry(QtCore.QRect(30, 120, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_date.setFont(font)
        self.lb_date.setObjectName("lb_date")
        self.date_appointment = QtWidgets.QDateEdit(UpdateAppointmentWindow)
        self.date_appointment.setGeometry(QtCore.QRect(160, 120, 150, 25))
        self.date_appointment.setObjectName("date_appointment")
        self.lb_time = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_time.setGeometry(QtCore.QRect(30, 160, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_time.setFont(font)
        self.lb_time.setObjectName("lb_time")
        self.time_appointment = QtWidgets.QTimeEdit(UpdateAppointmentWindow)
        self.time_appointment.setGeometry(QtCore.QRect(160, 160, 150, 25))
        self.time_appointment.setObjectName("time_appointment")
        self.lb_status = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_status.setGeometry(QtCore.QRect(30, 200, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_status.setFont(font)
        self.lb_status.setObjectName("lb_status")
        self.cb_status = QtWidgets.QComboBox(UpdateAppointmentWindow)
        self.cb_status.setGeometry(QtCore.QRect(160, 200, 150, 25))
        self.cb_status.setObjectName("cb_status")
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.lb_reason = QtWidgets.QLabel(UpdateAppointmentWindow)
        self.lb_reason.setGeometry(QtCore.QRect(30, 240, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_reason.setFont(font)
        self.lb_reason.setObjectName("lb_reason")
        self.txt_reason = QtWidgets.QTextEdit(UpdateAppointmentWindow)
        self.txt_reason.setGeometry(QtCore.QRect(160, 240, 300, 80))
        self.txt_reason.setObjectName("txt_reason")
        self.bt_save = QtWidgets.QPushButton(UpdateAppointmentWindow)
        self.bt_save.setGeometry(QtCore.QRect(130, 340, 100, 30))
        self.bt_save.setObjectName("bt_save")
        self.bt_cancel = QtWidgets.QPushButton(UpdateAppointmentWindow)
        self.bt_cancel.setGeometry(QtCore.QRect(260, 340, 100, 30))
        self.bt_cancel.setObjectName("bt_cancel")

        self.retranslateUi(UpdateAppointmentWindow)

    def retranslateUi(self, UpdateAppointmentWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateAppointmentWindow.setWindowTitle(_translate("UpdateAppointmentWindow", "Actualizar Cita"))
        self.lb_title.setText(_translate("UpdateAppointmentWindow", "Actualizar Cita"))
        self.lb_patient.setText(_translate("UpdateAppointmentWindow", "Paciente:"))
        self.lb_patient_name.setText(_translate("UpdateAppointmentWindow", "Nombre del Paciente"))
        self.lb_date.setText(_translate("UpdateAppointmentWindow", "Fecha:"))
        self.date_appointment.setDisplayFormat(_translate("UpdateAppointmentWindow", "dd/MM/yyyy"))
        self.lb_time.setText(_translate("UpdateAppointmentWindow", "Hora:"))
        self.time_appointment.setDisplayFormat(_translate("UpdateAppointmentWindow", "HH:mm"))
        self.lb_status.setText(_translate("UpdateAppointmentWindow", "Estado:"))
        self.cb_status.setItemText(0, _translate("UpdateAppointmentWindow", "Pendiente"))
        self.cb_status.setItemText(1, _translate("UpdateAppointmentWindow", "Confirmada"))
        self.cb_status.setItemText(2, _translate("UpdateAppointmentWindow", "Cancelada"))
        self.cb_status.setItemText(3, _translate("UpdateAppointmentWindow", "Completada"))
        self.lb_reason.setText(_translate("UpdateAppointmentWindow", "Motivo:"))
        self.bt_save.setText(_translate("UpdateAppointmentWindow", "Guardar"))
        self.bt_cancel.setText(_translate("UpdateAppointmentWindow", "Cancelar"))
