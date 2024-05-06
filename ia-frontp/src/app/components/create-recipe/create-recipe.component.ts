import { Component, OnInit } from '@angular/core';
import { Recipe } from '../../interface/recipe';

@Component({
  selector: 'app-create-recipe',
  templateUrl: './create-recipe.component.html',
  styleUrls: ['./create-recipe.component.css']
})
export class CreateRecipeComponent implements OnInit {

  scontent: string | null = null; // Corregido aquí

  ngOnInit() {
    this.scontent = localStorage.getItem('savedRecipe'); // Corregido aquí
  }

  recipe: Recipe = {
    name: '',
    date: new Date(),
    description: '',
    content: ''
  };

  constructor() {}

  submitForm() {
    this.recipe.content = this.scontent || '';
    console.log('Receta guardada:', this.recipe);
    localStorage.setItem('savedRecipe', JSON.stringify(this.recipe));
  }
}
