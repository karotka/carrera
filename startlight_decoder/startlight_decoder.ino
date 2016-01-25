const int dataInPin = 2;

boolean wordChange = false;

long Word = 0;
long currentWord = 0;

unsigned long intervalMicros = 0;
unsigned long previousMicros = 0;
unsigned long currentMicros  = 0;

void setup() {
    Serial.begin(115200);
    pinMode(dataInPin, INPUT);
    attachInterrupt(0, manchesterDecode, CHANGE);
    DDRC  = 0b01111110;
    PORTC = 0b00000000;
}

void loop() {
    if(wordChange == true) {
        wordChange = false;
        changeLed();

        Serial.print(Word, BIN);
        Serial.print("\t");
        Serial.println(Word);
        delay(200);
    }
}

void changeLed() {
    switch (Word) {
    case 4111:
        PORTC = B00000000;
        break;
    case 6159:
        PORTC = B00000001;
        break;
    case 5135:
        PORTC = B00000011;
        break;
    case 7183:
        PORTC = B00000111;
        break;
    case 4623:
        PORTC = B00001111;
        break;
    case 6671:
        PORTC = B00011111;
        break;
    }
}

void manchesterDecode() {
    currentMicros = micros();
    intervalMicros = currentMicros - previousMicros;
    if (intervalMicros > 75 && intervalMicros < 125) {
        previousMicros = currentMicros;
        currentWord = currentWord << 1;
        if (digitalRead(dataInPin) == LOW) {
            bitSet(currentWord, 0);
        }
        return;
    }
    if (intervalMicros > 6000) {
        Word = currentWord;
        currentWord = 0;
        bitSet(currentWord, 0);
        wordChange = true;
        previousMicros = currentMicros;
        return;
    }
}
