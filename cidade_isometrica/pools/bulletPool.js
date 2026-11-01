import { CONFIG } from '../config.js';

export class BulletPool {
  constructor(){
    this.pool = Array.from({length: CONFIG.POOL_BULLET}, () => ({active:false, x:0, y:0, vx:0, vy:0, life:0}));
  }
  acquire(){
    for(const b of this.pool){ if(!b.active){ return b; } }
    // fallback: create new if pool exhausted
    const b = {active:true, x:0, y:0, vx:0, vy:0, life:0};
    this.pool.push(b); return b;
  }
  release(b){ b.active = false; }
}

export const bulletPool = new BulletPool();
