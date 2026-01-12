#!/bin/bash

# Rasa Chatbot Başlatma Script'i

echo "🚀 Rasa E-Ticaret Chatbot Başlatılıyor..."
echo ""

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Port kontrolü
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "❌ Port $1 zaten kullanımda!"
        echo "   Çözüm: lsof -ti:$1 | xargs kill -9"
        return 1
    else
        echo "✅ Port $1 müsait"
        return 0
    fi
}

echo "📡 Port kontrolleri..."
check_port 5005 || exit 1
check_port 5055 || exit 1
check_port 8080 || exit 1

echo ""
echo "📦 Model kontrolü..."
if [ ! -d "models" ] || [ -z "$(ls -A models/*.tar.gz 2>/dev/null)" ]; then
    echo "⚠️  Model bulunamadı. Eğitim başlatılıyor..."
    rasa train
else
    echo "✅ Model mevcut"
fi

echo ""
echo "${GREEN}🎯 Servisler başlatılıyor...${NC}"
echo ""

# Rasa server'ı arka planda başlat
echo "${BLUE}[1/3]${NC} Rasa Server başlatılıyor (Port 5005)..."
rasa run --enable-api --cors "*" > logs/rasa.log 2>&1 &
RASA_PID=$!
sleep 3

# Action server'ı arka planda başlat
echo "${BLUE}[2/3]${NC} Action Server başlatılıyor (Port 5055)..."
rasa run actions > logs/actions.log 2>&1 &
ACTIONS_PID=$!
sleep 2

# Web widget server'ı başlat
echo "${BLUE}[3/3]${NC} Web Widget başlatılıyor (Port 8080)..."
cd widget && python -m http.server 8080 > ../logs/widget.log 2>&1 &
WIDGET_PID=$!
cd ..

echo ""
echo "${GREEN}✅ Tüm servisler başlatıldı!${NC}"
echo ""
echo "📍 Erişim Noktaları:"
echo "   🤖 Rasa API:    http://localhost:5005"
echo "   ⚡ Actions:     http://localhost:5055"
echo "   🌐 Web Widget:  http://localhost:8080"
echo ""
echo "📋 Process ID'leri:"
echo "   Rasa: $RASA_PID"
echo "   Actions: $ACTIONS_PID"
echo "   Widget: $WIDGET_PID"
echo ""
echo "🛑 Durdurmak için: kill $RASA_PID $ACTIONS_PID $WIDGET_PID"
echo "   veya: ./scripts/stop.sh"
echo ""
echo "📊 Loglar: logs/ klasöründe"
echo ""
echo "${GREEN}🎉 Chatbot hazır! http://localhost:8080 adresine gidin${NC}"
