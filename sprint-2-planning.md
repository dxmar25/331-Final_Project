# Sprint 2 Planning Meeting

This documents includes the sprint goal and our sprint 2 backlog 

## Sprint Goal

The goal for sprint 2, is to connect backend PostgreSQL database to the website hosted on vercel, with data being displayed from the database to various parts of the website, enable integration with multiple APIs for auth, translation, and weather, as well as layout changes to menu board and items.

## Sprint Backlog

| Task                                                          | Task No | Priority (1-5) | Dependencies | Estimate Time (hr) | Status     |
|---------------------------------------------------------------|---------|----------------|--------------|---------------------|------------|
| Google OAuth2 setup                                           | 0       | 2              |              | 1                   | Not started|
| Google OAuth2 implementation/connection                       | 1       | 2              | 0            | 1                   | Not started|
| Authentication using Google OAuth2 for Cashiers               | 2       | 2              | 1            | 1                   | Not started|
| Authentication using Google OAuth2 for Managers               | 3       | 2              | 1            | 1                   | Not started|
| Authentication using Google OAuth2 for Customers              | 4       | 2              | 1            | 1                   | Not started|
| Google OAuth2 testing                                         | 5       | 2              | 0,1          | 4                   | Not started|
| Google Translate API Setup                                    | 6       | 2              |              | 1                   | Not started|
| Google Translate Implementation                               | 7       | 2              | 6            | 2                   | Not started|
| Translate to native price (us, peso, canadian)?               | 8       | 3              | 7            | 4                   | Not started|
| OpenWeather setup                                             | 9       | 2              |              | 1                   | Not started|
| OpenWeather implementation/connection                         | 10      | 2              | 9            | 2                   | Not started|
| Open Weather Price adjustment? Aka surge pricing.             | 11      | 2              | 10           | 6                   | Not started|
| Surge Pricing testing                                         | 12      | 2              | 10,11        | 4                   | Not started|
| Connection of SQL queries to Managers/analytics               | 13      | 1              | 20           | 4                   | Not started|
| Button validation with manager page                           | 14      | 3              | 14           | 2                   | Not started|
| Unit testing for SQL queries for manager page                 | 15      | 1              | 14           | 2                   | Not started|
| Front End: Base design of menu board                          | 16      | 1              |              | 8                   | Not started|
| Button placement for menu board in welcome screen             | 17      | 1              |              | 1                   | Not started|
| Dynamic updates of the menu board                             | 18      | 1              | 17           | 4                   | Not started|
| Backend: CRUD for singular menu item and R for all menu-items | 19      | 3              |              | 2                   | Not started|
| Partial special functions                                     | 20      | 3              |              | 2                   | Not started|
| Unit tests for user CRUD                                      | 21      | 4              |              | 2                   | Not started|


