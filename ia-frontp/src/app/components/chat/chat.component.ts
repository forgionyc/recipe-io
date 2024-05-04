import { Component, OnInit } from '@angular/core';
import { ChatMessage } from '../../interface/chat-message.interface';
import { AuthService } from '../../service-api/auth.service';
import { PredictionModel } from '../../models/prediction.model';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit{
  messages: ChatMessage[] = [];
  newMessage: string = '';
  showBackground: boolean = true;
  savedUsername = localStorage.getItem('username') ?? 'User';
  selectedImageUrl: string | ArrayBuffer | null = null;
  selectedImageUrlForMessage: string | ArrayBuffer | null = null;


  constructor(private authService: AuthService) { 
    this.authService.formDataPrediction = new PredictionModel();
  }

  ngOnInit(): void {
    this.savedUsername;
  }

  sendMessage() {
    this.selectedImageUrl = null;
    if (this.newMessage.trim() !== '') {
      this.messages.push({
        sender: this.savedUsername,
        content: this.newMessage,
        image: this.selectedImageUrlForMessage,
        timestamp: new Date()
      });
      this.showBackground = true;
      // Respuesta del bot
      this.botResponse();
      this.selectedImageUrlForMessage = null;
      this.newMessage = '';
    }
  }

  botResponse() {
    // Simulación de respuesta del bot
    const botMessage: ChatMessage = {
      sender: 'RecipeBot',
      content: '¡Hola! Soy un bot y estoy aquí para ayudarte. La imagen que acabas de ingresar es '+  this.authService.formDataPrediction.predictedClass 
      + " con una precision de: "+  this.authService.formDataPrediction.confidenceScore +" %" ,
      timestamp: new Date()
    };
    this.messages.push(botMessage);
  }

  onFileSelected(event: any) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const reader = new FileReader();
      reader.readAsDataURL(selectedFile);
      reader.onload = () => {
          this.selectedImageUrl = reader.result;
          this.selectedImageUrlForMessage = reader.result;
      };
    }
    this.authService.postImage(selectedFile).subscribe(
        (response) => {
            console.log('Respuesta del servidor:', response);
            this.authService.formDataPrediction = response;
        },
        (error) => {
            console.error('Error al enviar la imagen:', error);
        }
    );
  }
  
  
}

