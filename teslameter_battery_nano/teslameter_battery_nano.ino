    #define SCLK_HIGH   0x20  //bit 5
    #define SCLK_LOW    0xDF  //~bit 5
    #define RCLK_HIGH   0x40  //bit 6
    #define RCLK_LOW    0xBF  //~bit 6
    #define DIO_HIGH    0x80  //bit 7
    #define DIO_LOW    0x7F  //~bit 7
    #define DIO_HIGH    0x80  //bit 7
    #define DIO_LOW    0x7F  //~bit 7
    #define RED_HIGH    0x01  // ~bit0 -> PORTB, pin8
    #define RED_LOW    0xFE  // ~bit0
    #define GREEN_HIGH    0x02  // ~bit1 -> PORTB, pin9
    #define GREEN_LOW    0xFD  // ~bit1
    #define BUFFERLEN  650
    #define OFFSET_bit  0x10  // bit 4
    unsigned char LED_0F[] =
    {// 0  1   2    3  4 5   6    7  8 9   A    b  C    d    E    F    -
      0xC0,0xF9,0xA4,0xB0,0x99,0x92,0x82,0xF8,0x80,0x90,0x8C,0xBF,0xC6,0xA1,0x86,0xFF,0xbf
    };
    unsigned char LED[4];
    byte pinSCLK = 5;
    byte pinRCLK = 6;
    byte pinDIO = 7;
    byte pinOffset = 4;
    byte pinRed = 8;
    byte pinGreen = 9;
    int cnt = 0;
    int avals[BUFFERLEN];
    float value = 0.0;
    long sum = 0;
    long finalsum = 0;
    float offset = 0;
    byte sign = 0;
    byte newsign = 0;
    
    void setup ()
    {
      pinMode(pinSCLK, OUTPUT);
      pinMode(pinRCLK, OUTPUT);
      pinMode(pinDIO, OUTPUT); 
      pinMode(pinRed, OUTPUT);
      pinMode(pinGreen, OUTPUT);
      pinMode(pinOffset, INPUT_PULLUP); 
      Serial.begin(19200);
    }
    
    void loop()
    {
        avals[cnt] = analogRead(A6)-511;
        sum += avals[cnt];
        cnt += 1;
            
        if (cnt == BUFFERLEN)
        {
          finalsum = sum;
          value = (sum-offset)*5.0/BUFFERLEN/1023*31.25;
          //Serial.println(value);
          if (value > 0)
          {
            PORTB &= GREEN_LOW;
            PORTB |= RED_HIGH;
          }
          else
          {
            value = -value;
            PORTB &= RED_LOW;
            PORTB |= GREEN_HIGH;
          }
          cnt = 0;
          sum = 0;
        }
        /* //Serial.println(avals[cnt]);
        if (cnt % 3 == 0)
        {
          //Serial.print(offset);
          //Serial.print(" ");
          Serial.println(avals[cnt]);          
        }
        */
        LED4_Display(value);
        
        if ((PIND&OFFSET_bit)==0) //(digitalRead(pinOffset) == 0)
          offset = finalsum;
    }
   
    void LED4_Display (float value)
    {
        unsigned int charactervalue;
        unsigned char character;
        unsigned int ivalue = (int)(value*100);
        
        for (byte digit = 0; digit < 4; digit++)
        {
            charactervalue = ivalue % 10;
            ivalue = ivalue / 10;
            
            if ((digit == 3) && ( charactervalue==0 ))
            {
              charactervalue=15;
            }
            character = LED_0F[charactervalue];
            if (digit == 2)
            {
                character &= ~0x80;  // dot on
            }
            DIGIT_OUT(character, digit);
        }
        // digit 3 off again. -> keep intensity of all 4 equal
        delayMicroseconds(25);
        DIGIT_OUT(0xFF, 3);
    }


void DIGIT_OUT(unsigned char X, byte digit)
{
  LED_OUT(X);
  LED_OUT(1<<digit);
  PORTD &= RCLK_LOW;
  PORTD |= RCLK_HIGH;
}

void LED_OUT(unsigned char X)
{
  unsigned char i;
  for(i=8;i;i--)
  {
    PORTD &= SCLK_LOW;
    PORTD &= DIO_LOW;
    if (X&0x80) PORTD |= DIO_HIGH;
    PORTD |= SCLK_HIGH;
    X<<=1;
  }
}

