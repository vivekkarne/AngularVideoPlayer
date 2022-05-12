import { HttpClient } from '@angular/common/http';
import { BackendService } from './../services/backend.service';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-upload-form',
  templateUrl: './upload-form.component.html',
  styleUrls: ['./upload-form.component.css']
})
export class UploadFormComponent implements OnInit {

  uploadForm = new FormGroup({
    fileControl: new FormControl('', [Validators.required]),
    fileSource: new FormControl('', [Validators.required])
  });

  oid_orig: string = '';
  rst: boolean = false;

  constructor(private http: HttpClient, private backend: BackendService) {

  }


  get fileControl(): any { return this.uploadForm.get('fileControl'); }

  ngOnInit(): void {

  }

  onFileChange(event: any) {
    if(event.target.files.length > 0) {
      const file: File = event.target.files[0];
      this.uploadForm.patchValue({
        fileSource: file
      })
    }
  }

  onSubmit(): void {
    const formData = new FormData();
    formData.append('video', this.uploadForm.get('fileSource')!.value );
    //Reset the video source
    this.oid_orig = '';
    this.rst = false;
    this.backend.uploadFile(formData).subscribe(data => {
      if(data.id) {
        this.oid_orig = data.id;
      }
    });
  }

  clearForm(): void {
    this.uploadForm.reset();
    this.oid_orig = '';
    this.rst = true;
  }
}
