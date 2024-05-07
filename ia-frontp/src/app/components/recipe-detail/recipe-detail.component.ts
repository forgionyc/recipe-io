import { Component, OnInit } from '@angular/core';
import { Recipe } from '../../interface/recipe';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  styleUrl: './recipe-detail.component.css',
})
export class RecipeDetailComponent implements OnInit {
  recipe!: Recipe;

  constructor() {}

  ngOnInit(): void {
    //EJEMPLO!
    this.recipe = {
      name: 'Tuna Stuffed Potatoes',
      date: new Date(),
      description: 'Tuna with potatotes',
      content: `
      **Tuna Stuffed Potatoes:**
      
      **Ingredients:**
      - 1 large potato
      - 1 can of tuna in water (you can use tuna in oil if you prefer)
      - 1/4 onion, diced
      - 1/4 red bell pepper, diced
      - 2 tablespoons mayonnaise
      - Salt and pepper to taste
      - Grated cheese (optional)
      
      **Instructions:**
      
      1. Preheat the oven to 200°C (390°F).
      
      2. Wash the potato thoroughly and dry it with a clean cloth. Poke the potato several times with a fork to allow it to cook evenly.
      
      3. Place the potato on a baking tray and put it in the preheated oven. Bake for approximately 45-60 minutes, or until tender and you can easily pierce it with a fork.
      
      4. While the potato is baking, prepare the filling. In a bowl, mix the drained tuna, diced onion, diced red bell pepper, mayonnaise, salt, and pepper to taste. Mix until well combined.
      
      5. Once the potato is cooked, remove it from the oven and cut it in half lengthwise. Using a spoon, scoop out some of the potato pulp, leaving about a 1 cm border around to maintain its shape.
      
      6. Mix the potato pulp with the tuna mixture you prepared earlier.
      
      7. Stuff the potato halves with the tuna and potato mixture. If desired, sprinkle some grated cheese on top of the stuffed potatoes.
      
      8. Return the stuffed potatoes to the oven and bake for another 10-15 minutes, or until the cheese is melted and they are heated through.
      
      9. Serve the hot Tuna Stuffed Potatoes and enjoy!
      
    `,
    };
  }
}
