import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.scss']
})
export class MessageComponent implements OnInit {

  constructor(private http:HttpClient) { }

  api = "http://127.0.0.1:8000"

  isLoading = false

  message = ""

  result = ""

  lines: any
  
  ngOnInit(): void {
  }

  run(){
    this.isLoading = true
    this.http.post<any>(`${this.api}/message`, {"SubscriptionId": localStorage.getItem('sub_id'), "Description": this.message})
    .subscribe(response => {
      console.log(response)
      debugger
      this.result = JSON.stringify(response)
      this.lines = response.split(/\r?\n/)
      this.isLoading = false
    })
  }

}
