import { Component } from '@angular/core';
import { BbService } from './bb.service';
import { OnInit } from '@angular/core';


@Component({
  selector: 'app-bb-list',
  imports: [],
  templateUrl: './bb-list.component.html',
  styleUrl: './bb-list.component.css'
})

export class BbListComponent implements OnInit {
  protected bbs: any[] = [];
  constructor(private bbservice: BbService) {}

  ngOnInit() {
    this.bbservice.getBbs().subscribe(
      (bbs: Object[]) => {this.bbs = bbs;}
    );
  }
}
