const int dataPin = 2;       
const int dataInPin = 2; 

const int red1Pin =  8;                      
const int red2Pin =  9;                      
const int red3Pin = 10;                        
const int red4Pin = 11;                       
const int red5Pin = 12;

         
int wordCount = 0;                       
boolean wordChange = false;        
long currentWord = 0;                               
long Word = 0;                                      
long Words[11];                                    
unsigned long intervalMicros = 0;                   
unsigned long previousMicros = 0;
unsigned long currentMicros  = 0;

void setup() {               
  int ledPin;                          
    Serial.begin(115200);                                
    pinMode(dataPin, INPUT);                            
    attachInterrupt(0, manchesterDecode, CHANGE);               
  for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++){     
    pinMode(ledPin, OUTPUT);                          
    digitalWrite( ledPin, LOW);}      
}                                       
                                           
void loop() {                                         
    if( wordChange == true ){                        
        wordChange = false;                             
        if( Word > 4000 )                                
            wordCount = 1;                                  
      Words[ wordCount ] = Word;                        
      wordCount++;
    
    
    }                                     
    if ( wordCount == 11 ){                             
    for (wordCount=1; wordCount < 11; wordCount++){   
      Serial.print( wordCount, DEC );                 
      Serial.print( "\t" );                           
      Serial.println( Words[ wordCount ], BIN );
    }     
    Serial.println("---------------------------");    
    wordCount = 1;                                    
    delay(100);

     int ledPin;                                           
  if( wordChange == true ){              
    Serial.print("Word:");               
    Serial.println(Word);               
    wordChange = false;                                 
    switch ( Word ) {                                  
      case 4111:                                        // Binary: 1000000001111 programming data word: command 16, value 0                                  
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, LOW );                  
        break;                                         
      case 6159:                                        // Binary: 1100000001111 programming data word: command 16, value 1
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, LOW );                  
        digitalWrite( red1Pin, HIGH );                  
        break;                                          
      case 5135:                                        // Binary: 1010000001111 programming data word: command 16, value 2
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, LOW );                  
        digitalWrite( red1Pin, HIGH );                  
        digitalWrite( red2Pin, HIGH );                  
        break;                                          
      case 7183:                                        // Binary: 1110000001111 programming data word: command 16, value 3
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, LOW );                  
        for (ledPin=red1Pin; ledPin<=red3Pin; ledPin++) 
          digitalWrite( ledPin, HIGH );                 
        break;                                          
      case 4623:                                        // Binary: 1000100001111 programming data word: command 16, value 4
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, LOW );                  
        for (ledPin=red1Pin; ledPin<=red4Pin; ledPin++) 
          digitalWrite( ledPin, HIGH );                 
        break;                                          
      case 6671:                                        // Binary: 1101000001111 programming data word: command 16, value 5
        for (ledPin=red1Pin; ledPin<=red5Pin; ledPin++) 
          digitalWrite( ledPin, HIGH );                 
        break;                                          
    }                                                   
  }     
    
    
    
    }                                  
}                                        

void manchesterDecode(){                              
    currentMicros = micros();                           
    intervalMicros = currentMicros - previousMicros;   
    if (intervalMicros > 75 && intervalMicros < 125) {   
        previousMicros = currentMicros;                   
        currentWord = currentWord << 1;                   
        if ( digitalRead( dataPin ) == LOW )              
            bitSet( currentWord,0 );                        
        return;
    }                                         
    if ( intervalMicros > 6000 ) {                      
        Word = currentWord;                               
        currentWord = 0;                                  
        bitSet( currentWord,0 );                          
        wordChange = true;                                 
        previousMicros = currentMicros;                   
        return;
    }                                                          
}                                

