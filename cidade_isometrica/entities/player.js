import { CONFIG } from '../config.js';
import { iso, shade, box } from '../utils.js';
import { bulletPool } from '../pools/bulletPool.js';

export class Player {
  constructor(x, y){
    this.x = x; this.y = y;
    this.speed = CONFIG.PLAYER_SPEED;
    this.health = CONFIG.PLAYER_MAX_HEALTH;
    this.fx = 1; this.fy = 0;
    this.walk = 0;
    this.shootCd = 0;
  }
  update(dt, keys, blocked){
    let dx=0, dy=0;
    if(keys.ArrowUp){dx-=1; dy-=1;}
    if(keys.ArrowDown){dx+=1; dy+=1;}
    if(keys.ArrowLeft){dx-=1; dy+=1;}
    if(keys.ArrowRight){dx+=1; dy-=1;}
    if(dx||dy){
      const l = Math.hypot(dx, dy);
      this.fx = dx/l; this.fy = dy/l;
      const nx = this.x + dx/l * this.speed * dt;
      const ny = this.y + dy/l * this.speed * dt;
      if(!blocked(nx, this.y)) this.x = nx;
      if(!blocked(this.x, ny)) this.y = ny;
      this.walk += dt*12;
    }
    this.shootCd -= dt;
    if(keys[' '] && this.shootCd <= 0){
      this.shootCd = CONFIG.SHOOT_COOLDOWN;
      const b = bulletPool.acquire();
      b.active = true;
      b.x = this.x + this.fx*0.5;
      b.y = this.y + this.fy*0.5;
      b.vx = this.fx * CONFIG.BULLET_SPEED;
      b.vy = this.fy * CONFIG.BULLET_SPEED;
      b.life = CONFIG.BULLET_LIFE;
    }
  }
  draw(ctx){
    const bob = Math.sin(this.walk)*1.5;
    box(ctx, this.x-0.2, this.y-0.2, CONFIG.PLAYER_SIZE, CONFIG.PLAYER_SIZE, CONFIG.PLAYER_HEIGHT+bob, '#00e5ff', '#0097a7', '#006064');
    const [hx, hy] = iso(this.x, this.y, CONFIG.PLAYER_HEIGHT+bob);
    ctx.beginPath(); ctx.arc(hx, hy-4, 4, 0, Math.PI*2); ctx.fillStyle = '#ffe0b2'; ctx.fill();
  }
}
