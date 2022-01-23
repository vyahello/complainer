import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Validators } from '@angular/forms';
import { FormGroup, FormBuilder } from 'ngx-strongly-typed-forms';
import { LoginService } from './login.service';
import { LoginFormModel } from './login.model';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterExtService } from 'src/app/shared/rouer-ext.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup<LoginFormModel>;
  returnUrl: string;
  @Output() emitter: EventEmitter<string> = new EventEmitter<string>();
  whoAmI: string = "";

  constructor(private fb: FormBuilder, private loginService: LoginService, private route: ActivatedRoute, private router: Router,private routerService: RouterExtService) { 
    if(localStorage.getItem('token')) {
      this.router.navigate(['complaints'])
    }
  }

  ngOnInit(): void {
    localStorage.removeItem('token');
    this.loginForm = this.fb.group<LoginFormModel>({
      email: ['', Validators.required],
      password: ['', Validators.required],
    })
  }

  changeWhoAmI(choice) {
    console.log(choice)
    this.whoAmI = choice
  }

  login() {
    this.loginService.login(this.loginForm.value, this.whoAmI).subscribe(res => {
      this.loginService.setTToken(res['token']);
      this.loginService.setRole(res["role"])
      window.location.reload()

      this.router.navigate(['complaints']);
      

    })
  }

}
