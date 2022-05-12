import { BackendService } from './../services/backend.service';
import { Component, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { TOUCH_BUFFER_MS } from '@angular/cdk/a11y/input-modality/input-modality-detector';

@Component({
  selector: 'app-video-player',
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.css']
})
export class VideoPlayerComponent implements OnInit {

  @Input() oid_orig = '';
  @Input() rst = true;

  src: string | undefined;
  gscale_src: string | undefined;
  tabGroup: any | undefined;

  isGrayscale: boolean = false;

  constructor() {

  }

  ngOnInit(): void {
  }

  convertGray(tabGroup: any): void {
    this.isGrayscale = true;
    this.gscale_src = "http://localhost:5000/gscale/"+this.oid_orig;
    this.tabGroup = tabGroup;
    tabGroup.selectedIndex = 1;
  }

  
  ngOnChanges(): any {
    if(this.oid_orig !== '') {
      this.src = "http://localhost:5000/files/"+this.oid_orig;
      console.log(this.oid_orig);
    }
    else if(this.rst == true) {
      this.tabGroup.selectedIndex = 0;
    }
    this.isGrayscale = false;
  }


}
