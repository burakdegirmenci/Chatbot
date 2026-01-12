#!/bin/bash

# Rasa Chatbot Durdurma Script'i

echo "🛑 Rasa servisleri durduruluyor..."

# Port'larda çalışan process'leri bul ve durdur
echo "Cleaning up ports..."

# Port 5005 (Rasa)
if lsof -Pi :5005 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "  Stopping Rasa server (5005)..."
    lsof -ti:5005 | xargs kill -9
fi

# Port 5055 (Actions)
if lsof -Pi :5055 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "  Stopping Actions server (5055)..."
    lsof -ti:5055 | xargs kill -9
fi

# Port 8080 (Widget)
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "  Stopping Web widget (8080)..."
    lsof -ti:8080 | xargs kill -9
fi

# Python process'lerini temizle
pkill -f "rasa run" 2>/dev/null
pkill -f "http.server" 2>/dev/null

echo "✅ Tüm servisler durduruldu"
