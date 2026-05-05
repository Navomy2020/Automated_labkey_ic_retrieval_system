# 🔬 Digital Lab Key & IC Retrieval System

## 📌 Overview
The Digital Lab Key & IC Retrieval System is an IoT-based solution designed to automate the tracking and management of laboratory keys and electronic components (ICs).

Traditional lab management using manual registers is prone to:
- Human errors  
- Misplacement of keys/components  
- Lack of accountability  

This project integrates ESP32 hardware, RFID, barcode input, and a web-based backend to provide a real-time, secure, and efficient tracking system.

---

## 🚀 Features

- RFID-based identification of keys and ICs  
- Barcode input via mobile phone  
- Quantity selection using hardware buttons  
- ESP32-based IoT system with Wi-Fi  
- REST API backend  
- Web dashboard for monitoring  
- WhatsApp chatbot integration  
- Real-time validation feedback on LCD  

---

## 🏗️ System Architecture

Mobile Phone → ESP32 → Backend → Database → Dashboard

---

## ⚙️ Technologies Used

### Hardware
- ESP32  
- RFID Module (MFRC522)  
- LCD Display  
- Buttons & Buzzer  

### Software
- Arduino C++  
- Node.js (Backend)  
- MySQL  
- HTML/CSS/JS  
- Twilio API  

---

## 🔄 Working

1. User sends barcode via phone  
2. RFID identifies item  
3. Quantity selected using buttons  
4. ESP32 sends data to backend  
5. Backend validates and stores  
6. Response shown on LCD  
7. Dashboard displays logs  

---

## ⚠️ Limitations

- Requires Wi-Fi  
- Group tracking of ICs    
- No offline support  

---

## 🔮 Future Scope

- Mobile app  
- Offline support  
- Real-time updates  
- Advanced analytics  

---

## 👨‍💻 Team

Meenakshi Jeevan 
Mohammad Irfan
Nandana  Biju
Navomy Mariya Alex 
