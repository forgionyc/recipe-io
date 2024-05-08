import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { Recipe } from '../interface/recipe';
import { environment} from '../../environments/environment.prod';

@Injectable({
  providedIn: 'root',
})
export class RecipeService {
  private apiUrl = environment.apiUrl;;

  constructor(private http: HttpClient) {}

  // Método para crear una nueva receta
  createRecipe(recipeData: any) {
    console.log(this.apiUrl);
    return this.http.post(`${this.apiUrl}api/recipes/`, recipeData);
  }
  createUser(userData: any) {
    return this.http.post(`${this.apiUrl}api/users/`, userData);
  }

  getUserRecipes(username: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}api/users/${username}/recipes/`);
  }

  getRecipe(recipeId: number): Observable<Recipe> {
    return this.http.get<Recipe>(`${this.apiUrl}api/recipes/${recipeId}`);
  }
}
