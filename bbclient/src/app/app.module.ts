import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { registerLocaleData } from '@angular/common';
import localeRu from '@angular/common/locales/ru';
import localeRuExtra from '@angular/common/locales/extra/ru';
import { LOCALE_ID } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { BbListComponent } from './bb-list.component';
import { BbDetailComponent } from './bb-detail.component';
import { BbService } from './bb.service';

registerLocaleData(localeRu, 'ru', localeRuExtra);

const appRoutes: Routes = [
    {path: ':pk', component: BbDetailComponent},
    {path: '', component: BbListComponent}
];

@NgModule({
    declarations: [
    AppComponent,
    BbListComponent,
    BbDetailComponent
    ],
    imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    HttpClientModule,
    FormsModule
    ],
    providers: [
    BbService,
    {provide: LOCALE_ID, useValue: 'ru'}
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }