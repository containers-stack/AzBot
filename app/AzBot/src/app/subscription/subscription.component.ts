import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-subscription',
  templateUrl: './subscription.component.html',
  styleUrls: ['./subscription.component.scss']
})

export class SubscriptionComponent implements OnInit {

  constructor(private http:HttpClient) { }

  api = "http://127.0.0.1:8000"

  subs: Subscription[] = [];
  
  selectedSub: any;
  isLoading = true  
  
  ngOnInit(): void {
    this.isLoading = true
    this.http.get<Subscription[]>(`${this.api}/subscriptions`)
      .subscribe(response => {
        console.log(response)
        this.subs = response
        this.selectedSub = this.subs[0].id
        localStorage.setItem('sub_id', this.selectedSub);
        this.isLoading = false

      })
  }

  switchSub(event: any){
    console.log(`sub: ${this.selectedSub} selected`)
    localStorage.setItem('sub_id', this.selectedSub);

  }
}

interface Subscription {
  name: string,
  id: string
}
