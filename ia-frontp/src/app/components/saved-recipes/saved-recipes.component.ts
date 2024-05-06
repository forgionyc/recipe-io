import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { Recipe } from '../../interface/recipe';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-saved-recipes',
  templateUrl: './saved-recipes.component.html',
  styleUrls: ['./saved-recipes.component.css']
})
export class SavedRecipesComponent {
  savedRecipes: Recipe[] = [
    { name: 'Recipe 1', date: new Date('2022-04-24'), content: 'Test',  description: 'Description of Recipe 1' },
    { name: 'Recipe 2', date: new Date('2022-04-24'), content: 'Test',  description: 'Description of Recipe 2' },
    { name: 'Recipe 3', date: new Date('2022-04-24'), content: 'Test',  description: 'Description of Recipe 3' }
  ];

  constructor(private router: Router, private dialog: MatDialog) { }

  displayedColumns: string[] = ['name', 'date', 'view', 'delete'];
  dataSource = new MatTableDataSource<Recipe>(this.savedRecipes);

  viewRecipe(recipe: Recipe) {
    this.router.navigate(['/recipe']);
  }

  openConfirmationDialog(recipe: Recipe): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '250px',
      data: { recipeName: recipe.name }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.delRecipe(recipe);
      }
    });
  }
  
  delRecipe(recipe: Recipe) {
    console.log('Deleting recipe:', recipe);
  }
}
